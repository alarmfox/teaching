package main

import (
	"bufio"
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"os"
	"time"

	"github.com/fsnotify/fsnotify"
)

type Task struct {
	Description string
	Completed   bool
	CheckFn     func(event fsnotify.Event) bool
}

type AdvancedTask struct {
	Description string
	Completed   bool
	CheckFn     func(ans string) bool
}

const dirPath = "data"

var start time.Time
var tasks = []*Task{
	{
		Description: "Create a file named 'example.txt' in 'data' folder",
		CheckFn: func(event fsnotify.Event) bool {

			return event.Op == fsnotify.Create && event.Name == "data/example.txt"

		},
	},
	{
		Description: "Change permissions of 'example.txt' to 0600 in the 'data' folder",
		CheckFn: func(event fsnotify.Event) bool {
			if event.Op != fsnotify.Chmod {
				return false
			}

			if event.Name != "data/example.txt" {
				return false
			}

			f, err := os.Stat("data/example.txt")
			if err != nil {
				return false
			}
			p := f.Mode().Perm()

			return p.String() == "-rw-------"
		},
	},
	{
		Description: "Delete the file named 'deleteme.txt' in 'data' folder",
		CheckFn: func(event fsnotify.Event) bool {
			if event.Op == fsnotify.Remove && event.Name == "data/deleteme.txt" {
				return true
			}
			return false
		},
	},
	// Add more tasks as needed
}

var advancedTasks = []*AdvancedTask{
	// Add advanced tasks here
	{
		Description: "What is the content of '.secret' file in the data folder?",
		CheckFn: func(ans string) bool {
			f, err := os.ReadFile("data/.secret")
			if err != nil {
				return false
			}
			return string(f) == ans
		},
	},
}

func listTasks() {
	for i, task := range tasks {
		status := "Not Completed"
		if task.Completed {
			status = "Completed"
		}
		fmt.Printf("%d. %s - %s\n", i+1, task.Description, status)
	}
}

func watchTasks() {
	watcher, err := fsnotify.NewWatcher()
	if err != nil {
		fmt.Println("ERROR", err)
		return
	}
	defer watcher.Close()

	done := make(chan bool)
	go func() {
		for {
			select {
			case event, ok := <-watcher.Events:
				if !ok {
					return
				}
				checkEvent(event)
			case err, ok := <-watcher.Errors:
				if !ok {
					return
				}
				fmt.Println("ERROR", err)
			}
		}
	}()

	if err := watcher.Add(dirPath); err != nil {
		fmt.Println("ERROR", err)
		return
	}
	<-done
}

func checkEvent(event fsnotify.Event) {
	for _, task := range tasks {
		if task.CheckFn(event) && !task.Completed {
			// Update this logic based on the actual completion criteria for each task
			fmt.Printf("Task completed: %s\n", task.Description)
			task.Completed = true
		}
	}
}

func main() {
	start = time.Now()
	first := true
	setupGameEnvironment()
	go watchTasks() // Start watching filesystem events in a goroutine

	for {
		if first && allTasksCompleted() {
			fmt.Println("Congratulations you have completed the simple tasks!")
			fmt.Println("Now it's time for the hard ones!")
			first = !first
		}
		if allAdvancedTasksCompleted() {
			fmt.Println("Congratulation! You won the game!")
			duration := time.Since(start)
			token := base64.StdEncoding.EncodeToString([]byte(duration.String()))
			fmt.Println("Your score token is ", token)
			fmt.Println("Submit to \"https://shell-game.capass.org/shell?code=<your-token>\" to get the score!")
		}
		showMenu()
		handleUserInput()

	}
}

func setupGameEnvironment() error {
	// Create a game_data directory
	if err := os.RemoveAll(dirPath); err != nil {
		return err
	}
	if err := os.Mkdir(dirPath, 0755); err != nil {
		return err
	}
	// Create an instructions file with initial tasks
	instructions := `Welcome to the Shell Game!
Your tasks:
1. Create a directory inside game_data named 'level1'.
2. Inside 'level1', create a file named 'task.txt' and write 'Shell Game' in it.
3. Change the permissions of 'task.txt' to read-only.
4. Find the hidden message in '.secret' and write it to 'secret_message.txt' in 'game_data'.

Good luck!
`
	if err := os.WriteFile(fmt.Sprintf("%s/deleteme.txt", dirPath), []byte(instructions), 0644); err != nil {
		return err
	}

	// Create a hidden file with a secret message
	b := make([]byte, 20)
	_, err := rand.Read(b)
	if err != nil {
		return err
	}
	s := base64.StdEncoding.EncodeToString(b)
	if err := os.WriteFile(fmt.Sprintf("%s/.secret", dirPath), []byte(s), 0644); err != nil {
		return err
	}

	return nil
}

func allTasksCompleted() bool {
	for _, task := range tasks {
		if !task.Completed {
			return false
		}
	}
	return true
}

func allAdvancedTasksCompleted() bool {

	for _, task := range advancedTasks {
		if !task.Completed {
			return false
		}
	}
	return true
}

func showSimpleTasks() {
	fmt.Println("Simple Tasks:")
	for i, task := range tasks {
		fmt.Printf("%d. %s - Completed: %t\n", i+1, task.Description, task.Completed)
	}
}

func askQuestions() {
	reader := bufio.NewReader(os.Stdin)
	for _, task := range advancedTasks {
		var answer string
		for !task.CheckFn(answer) {
			fmt.Printf("Question: %s\n", task.Description)
			fmt.Print("Your answer: ")
			answer, _ = reader.ReadString('\n')
			answer = answer[:len(answer)-1] // Remove the newline character
			fmt.Println("Your answer is:", answer)
		}
		task.Completed = true
	}
}

func showMenu() {
	// Show game menu
	fmt.Println("Game Menu")
	fmt.Println("0. Exit")
	fmt.Println("1. Show Simple Tasks")
	if allTasksCompleted() {
		fmt.Println("2. Start Advanced Tasks")
	}
}

func handleUserInput() {
	// Handle user input from the menu
	var choice int
	fmt.Scanln(&choice)

	switch choice {
	case 1:
		showSimpleTasks()
	case 2:
		askQuestions()
	case 0:
		fmt.Println("Exiting game.")
		os.Exit(0)
	default:
		fmt.Println("Invalid choice, please try again.")
	}
}
