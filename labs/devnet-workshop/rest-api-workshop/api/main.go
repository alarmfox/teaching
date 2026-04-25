package main

import (
	"context"
	"crypto/rand"
	"encoding/base64"
	"encoding/json"
	"errors"
	"flag"
	"fmt"
	"log/slog"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"strings"
	"sync"
	"time"
)

const (
	key          = "0InfNl5WZuR++sOUD4otAw=="
	session      = "sessionid"
	cookieLength = 20
)

type ctxKeyType int
type ctxValueType string

type Interface struct {
	Name        string `json:"name"`
	Address     string `json:"address"`
	Netmask     string `json:"netmask"`
	Description string `json:"description"`
	Status      string `json:"status"`
}

type Device struct {
	ID         int         `json:"id"`
	Serial     string      `json:"serial"`
	Model      string      `json:"model"`
	Type       string      `json:"type"`
	Interfaces []Interface `json:"interfaces"`
}

type SimpleDevice struct {
	ID     int    `json:"id"`
	Serial string `json:"serial"`
	Model  string `json:"model"`
	Type   string `json:"type"`
}

type Database struct {
	devices    map[int]Device
	mu         sync.RWMutex
	nextInt    int
	lastAccess time.Time
}

type ApiError struct {
	Message string `json:"message"`
}

var (
	sessions      map[string]*Database
	listenAddress = flag.String("listen-addr", "0.0.0.0:3000", "Listen address for the server")
	duration      = flag.Duration("clean-interval", time.Hour, "Interval to clean for session")
)

func main() {

	flag.Parse()

	var (
		logger = slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
			Level: slog.LevelDebug,
		}))
		ctx = context.Background()
	)

	slog.SetDefault(logger)

	sessions = make(map[string]*Database)

	server := makeHttpServer(ctx, *listenAddress)
	logger.Info("listening on", "address", *listenAddress)

	ctx, cancel := signal.NotifyContext(ctx, os.Interrupt, os.Kill)
	defer cancel()

	go func() {
		if err := server.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
			logger.Error("listen error", "error", err)
			os.Exit(2)
		}
	}()

	go func() {
		for {
			select {
			case <-ctx.Done():
				return
			case <-time.After(*duration):
				logger.Debug("cleaning up")
				cleanup()
			}
		}
	}()

	<-ctx.Done()

	logger.Info("got termination signal")

	if err := server.Shutdown(context.Background()); err != nil {
		logger.Error("error closing server", "error", err)
	}

}

func makeHttpServer(_ context.Context, httpServer string) *http.Server {

	mux := http.NewServeMux()

	var (
		getAllHandler = http.HandlerFunc(getAll)
		getOneHandler = http.HandlerFunc(getOne)
		deleteHandler = http.HandlerFunc(deleteDevice)
		createHandler = http.HandlerFunc(createDevice)
		updateHandler = http.HandlerFunc(updateDevice)
	)

	mux.Handle("GET /", setSession(getAllHandler))
	mux.Handle("POST /", setSession(auth(createHandler)))
	mux.Handle("GET /{id}", setSession(getOneHandler))
	mux.Handle("PUT /{id}", setSession(auth(updateHandler)))
	mux.Handle("DELETE /{id}", setSession(auth(deleteHandler)))

	server := http.Server{
		Addr:              httpServer,
		ReadHeaderTimeout: 10 * time.Second,
		IdleTimeout:       60 * time.Second,
		WriteTimeout:      5 * time.Second,
		Handler:           mux,
	}

	return &server
}

func getOne(w http.ResponseWriter, r *http.Request) {

	database, err := getDatabase(r.Context())
	if err != nil {
		writeJson(w, http.StatusInternalServerError, ApiError{Message: "Internal server error"})
		return
	}

	database.mu.RLock()
	defer database.mu.RUnlock()

	id := r.PathValue("id")
	idInt, err := strconv.Atoi(id)
	if err != nil {
		writeJson(w, http.StatusBadRequest, ApiError{Message: fmt.Sprintf("invalid id: %v", err)})
		return
	}
	device, exists := database.devices[idInt]

	if !exists {
		writeJson(w, http.StatusNotFound, ApiError{Message: fmt.Sprintf("device with id %q not found", id)})
		return
	}
	if err := writeJson(w, http.StatusOK, device); err != nil {
		writeJson(w, http.StatusInternalServerError, ApiError{Message: "internal server error"})
	}
}

func getAll(w http.ResponseWriter, r *http.Request) {

	database, err := getDatabase(r.Context())
	if err != nil {
		writeJson(w, http.StatusInternalServerError, ApiError{Message: "Internal server error"})
		return
	}
	database.mu.RLock()
	defer database.mu.RUnlock()
	results := make([]SimpleDevice, len(database.devices))
	i := 0
	for _, v := range database.devices {
		results[i] = toSimple(v)
		i += 1
	}
	if err := writeJson(w, http.StatusOK, results); err != nil {
		writeJson(w, http.StatusInternalServerError, ApiError{Message: "internal server error"})
	}
}

func deleteDevice(w http.ResponseWriter, r *http.Request) {

	database, err := getDatabase(r.Context())
	if err != nil {
		writeJson(w, http.StatusInternalServerError, ApiError{Message: "internal server error"})
		return
	}
	database.mu.Lock()
	defer database.mu.Unlock()
	id := r.PathValue("id")
	idInt, err := strconv.Atoi(id)
	if err != nil {
		writeJson(w, http.StatusBadRequest, ApiError{Message: fmt.Sprintf("invalid id: %v", err)})
		return
	}
	_, exists := database.devices[idInt]

	if !exists {
		http.Error(w, "Device not found", http.StatusNotFound)
		return
	}

	delete(database.devices, idInt)
	w.WriteHeader(http.StatusNoContent)
}

func createDevice(w http.ResponseWriter, r *http.Request) {
	database, err := getDatabase(r.Context())
	if err != nil {
		writeJson(w, http.StatusInternalServerError, ApiError{Message: "Internal server error"})
		return
	}
	database.mu.Lock()
	defer database.mu.Unlock()

	var device Device
	if err := json.NewDecoder(r.Body).Decode(&device); err != nil {
		writeJson(w, http.StatusBadRequest, ApiError{Message: fmt.Sprintf("malformed json body: %v", err)})
		return
	}
	defer r.Body.Close()

	id := database.nextInt
	device.ID = id
	database.devices[id] = device
	database.nextInt += 1

	if err := writeJson(w, http.StatusOK, device); err != nil {
		writeJson(w, http.StatusInternalServerError, ApiError{Message: "internal server error"})
	}

}
func updateDevice(w http.ResponseWriter, r *http.Request) {
	database, err := getDatabase(r.Context())
	if err != nil {
		writeJson(w, http.StatusInternalServerError, ApiError{Message: "Internal server error"})
		return
	}
	database.mu.Lock()
	defer database.mu.Unlock()

	id := r.PathValue("id")
	idInt, err := strconv.Atoi(id)
	if err != nil {
		writeJson(w, http.StatusBadRequest, ApiError{Message: fmt.Sprintf("invalid id: %v", err)})
		return
	}
	var device Device
	if err := json.NewDecoder(r.Body).Decode(&device); err != nil {
		writeJson(w, http.StatusBadRequest, ApiError{Message: fmt.Sprintf("malformed json body: %v", err)})
		return
	}
	defer r.Body.Close()

	_, exists := database.devices[idInt]

	if !exists {
		writeJson(w, http.StatusNotFound, ApiError{Message: fmt.Sprintf("device with id %q not found", id)})
		return
	}

	device.ID = idInt
	database.devices[idInt] = device
	if err := writeJson(w, http.StatusCreated, device); err != nil {
		writeJson(w, http.StatusInternalServerError, ApiError{Message: "internal server error"})
	}
}

func auth(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		token := r.Header.Get("Authorization")
		parts := strings.Split(token, " ")
		if len(parts) != 2 {
			writeJson(w, http.StatusUnauthorized, ApiError{Message: fmt.Sprintf("malformed authorization header")})
			return
		}

		if parts[0] != "Bearer" {
			writeJson(w, http.StatusUnauthorized, ApiError{Message: fmt.Sprintf("malformed authorization header. Must start with \"Bearer\"")})
			return
		}

		if parts[1] != key {
			writeJson(w, http.StatusUnauthorized, ApiError{Message: fmt.Sprintf("invalid key")})
			return
		}

		next.ServeHTTP(w, r)
	})
}

func writeJson(w http.ResponseWriter, statusCode int, data any) error {
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(statusCode)

	return json.NewEncoder(w).Encode(data)
}

func setSession(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		cookie, err := r.Cookie(session)
		if errors.Is(err, http.ErrNoCookie) {
			token := getToken(cookieLength)
			sessions[token] = initDatabase()
			cookie = &http.Cookie{
				Name:     session,
				Value:    token,
				HttpOnly: true,
			}
		} else if err != nil {
			slog.Error("error", "cookie error", err)
			return
		}

		ctx := context.WithValue(r.Context(), ctxKeyType(1), cookie.Value)
		r = r.WithContext(ctx)
		http.SetCookie(w, cookie)
		next.ServeHTTP(w, r)

	})

}

func getToken(length int) string {
	randomBytes := make([]byte, 32)
	_, err := rand.Read(randomBytes)
	if err != nil {
		panic(err)
	}
	return base64.StdEncoding.EncodeToString(randomBytes)[:length]
}

func getDatabase(ctx context.Context) (*Database, error) {
	token := ctx.Value(ctxKeyType(1))
	if token == nil {
		return nil, fmt.Errorf("error db not present")
	}

	database := sessions[token.(string)]
	if database == nil {
		database = initDatabase()
		sessions[token.(string)] = database
	}
	return database, nil

}

func toSimple(d Device) SimpleDevice {

	return SimpleDevice{
		ID:     d.ID,
		Serial: d.Serial,
		Model:  d.Model,
		Type:   d.Type,
	}
}

func initDatabase() *Database {
	db := make(map[int]Device)
	db[1] = Device{
		ID:     1,
		Serial: "CAT-2960-5483221",
		Model:  "Catalyst-2960x-48p",
		Type:   "SWL2",
		Interfaces: []Interface{
			{
				Name:        "VLAN1",
				Address:     "192.168.1.100",
				Netmask:     "255.255.255.0",
				Description: "A VLAN",
				Status:      "Administrative down",
			},
		},
	}
	db[2] = Device{
		ID:     2,
		Serial: "CAT-2960-5483221",
		Model:  "Catalyst-2960x-48p",
		Type:   "SWL2",
		Interfaces: []Interface{
			{
				Name:        "VLAN1",
				Address:     "192.168.1.100",
				Netmask:     "255.255.255.0",
				Description: "A VLAN",
				Status:      "Administrative down",
			},
		},
	}

	return &Database{
		devices: db,
		mu:      sync.RWMutex{},
		nextInt: len(db) + 1,
	}
}

func cleanup() {

	for id, session := range sessions {
		if time.Since(session.lastAccess) > time.Hour*5 {
			delete(sessions, id)
		}
	}
}
