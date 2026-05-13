use std::{
    collections::HashMap,
    fs::File,
    io::{BufRead, BufReader, Write},
    path::PathBuf,
};

use argon2::{
    Argon2,
    password_hash::{PasswordHash, PasswordHasher, PasswordVerifier, SaltString, rand_core::OsRng},
};
use chacha20poly1305::{ChaCha20Poly1305, Key, KeyInit, Nonce, aead::Aead};
use clap::{Parser, Subcommand, command};

struct Unlocked {
    key: Key,
}
struct Locked;

static DEFAULT_FNAME: &str = "password.db";

struct PasswordManager<State = Locked> {
    /// Stored master password hash
    master_hash: String,
    /// Passwords map
    passwords: HashMap<String, String>,
    state: State,
}

impl PasswordManager<Locked> {
    fn load(fname: &PathBuf) -> Result<PasswordManager<Locked>, std::io::Error> {
        let file = File::open(fname)?;
        let reader = BufReader::new(file);
        let mut lines = reader.lines();

        // The first line is always the master hash
        let master_hash = lines.next().ok_or_else(|| {
            std::io::Error::new(std::io::ErrorKind::InvalidData, "File is empty")
        })??;

        // The rest of the file contains key=value pairs
        let mut passwords = HashMap::new();
        for line in lines {
            let line = line?;
            if let Some((key, value)) = line.split_once('=') {
                passwords.insert(key.to_string(), value.to_string());
            }
        }

        Ok(PasswordManager {
            master_hash,
            passwords,
            state: Locked,
        })
    }

    // Fixed: This must return PasswordManager<Unlocked> to transition the typestate
    fn unlock(self, password: &str) -> Result<PasswordManager<Unlocked>, &'static str> {
        let parsed_hash =
            PasswordHash::new(&self.master_hash).map_err(|_| "Invalid hash format")?;

        Argon2::default()
            .verify_password(password.as_bytes(), &parsed_hash)
            .map_err(|_| "Invalid password")?;

        let mut key_bytes = [0u8; 32];
        Argon2::default()
            .hash_password_into(
                password.as_bytes(),
                parsed_hash.salt.unwrap().to_string().as_bytes(),
                &mut key_bytes,
            )
            .map_err(|_| "Key derivation failed")?;

        let crypto_key = Key::from_slice(&key_bytes).clone();
        let cipher = ChaCha20Poly1305::new(&crypto_key);

        // Decrypt the payload into memory
        let mut decrypted_passwords = HashMap::new();
        for (k, encrypted_hex) in &self.passwords {
            // In a real app, parse hex/base64 and extract the nonce.
            // For brevity, assuming hex decoding and a fixed 12-byte nonce derived from the key/salt
            let encrypted_bytes = hex::decode(encrypted_hex).map_err(|_| "Hex decode failed")?;
            let nonce = Nonce::from_slice(&key_bytes[0..12]); // Simplified nonce for example

            let plaintext = cipher
                .decrypt(nonce, encrypted_bytes.as_ref())
                .map_err(|_| "Decryption failed - data corrupted!")?;

            decrypted_passwords.insert(k.clone(), String::from_utf8(plaintext).unwrap());
        }

        // State transition: Return a new struct with the Unlocked state
        Ok(PasswordManager {
            master_hash: self.master_hash,
            passwords: decrypted_passwords,
            state: Unlocked { key: crypto_key },
        })
    }

    fn count(&self) -> usize {
        self.passwords.len()
    }
}

impl PasswordManager<Unlocked> {
    fn save(self, fname: &PathBuf) -> Result<(), std::io::Error> {
        let mut file = File::create(fname)?;
        writeln!(file, "{}", self.master_hash)?;

        let cipher = ChaCha20Poly1305::new(&self.state.key);
        // Simplified nonce for the example
        let nonce = Nonce::from_slice(&self.state.key[0..12]);

        for (key, plaintext_val) in &self.passwords {
            // ENCRYPT BEFORE SAVING!
            let ciphertext = cipher
                .encrypt(nonce, plaintext_val.as_bytes())
                .expect("Encryption failed");

            // Save as hex so it can be written as text
            writeln!(file, "{}={}", key, hex::encode(ciphertext))?;
        }

        Ok(())
    }

    fn add(&mut self, key: String, password: String) {
        self.passwords.insert(key, password);
    }

    fn delete(&mut self, key: &str) {
        self.passwords.remove(key);
    }

    fn list(&self) -> &HashMap<String, String> {
        &self.passwords
    }
}

#[derive(Parser)]
#[command(name = "passman")]
#[command(about = "A secure password manager demonstrating Rust typestates", version, long_about = None)]
struct Cli {
    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    /// Create a new password storage
    Init {
        /// The file path for the new store
        #[arg(short, long, default_value = DEFAULT_FNAME)]
        file: PathBuf,
    },

    /// Add a new password
    Add {
        /// The file path for the store
        #[arg(short, long, default_value = DEFAULT_FNAME)]
        file: PathBuf,

        /// Key to be inserted
        #[arg(short, long)]
        key: String,
    },

    /// Delete a password
    Delete {
        /// The file path for the store
        #[arg(short, long, default_value = DEFAULT_FNAME)]
        file: PathBuf,

        /// Key to be deleted
        #[arg(short, long)]
        key: String,
    },

    /// List all passwords
    List {
        /// The file path for the store
        #[arg(short, long, default_value = DEFAULT_FNAME)]
        file: PathBuf,

        /// Show passwords in clear text
        #[arg(short, long, default_value_t = false)]
        show: bool,
    },

    /// Count passwords
    Count {
        /// The file path for the store
        #[arg(short, long, default_value = DEFAULT_FNAME)]
        file: PathBuf,
    },
}

fn main() -> std::io::Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Init { file } => {
            let password = rpassword::prompt_password("Insert master password: ").unwrap();
            let check = rpassword::prompt_password("Confirm master password: ").unwrap();

            if password != check {
                eprintln!("Passwords do not match");
                return Ok(());
            }

            let salt = SaltString::generate(&mut OsRng);
            let argon2 = Argon2::default();

            let password_hash = argon2
                .hash_password(password.as_bytes(), &salt)
                .unwrap()
                .to_string();

            // Fixed: use create instead of open to actually create the DB file
            let mut file = File::create(file)?;
            writeln!(file, "{}", password_hash)?;

            println!("Database initialized successfully.");
            Ok(())
        }

        Commands::Add { file, key } => {
            let master_pw = rpassword::prompt_password("Insert master password: ").unwrap();
            let new_pw =
                rpassword::prompt_password(format!("Insert password for '{}': ", key)).unwrap();

            let confirn_new_pw =
                rpassword::prompt_password(format!("Confirm password for '{}': ", key)).unwrap();

            if new_pw != confirn_new_pw {
                eprintln!("Passwords for '{}' do not match", key);
                return Ok(());
            }

            let db = PasswordManager::load(&file).expect("Failed to load database");

            // Typestate in action: `db` is now `PasswordManager<Unlocked>`
            let mut unlocked_db = db.unlock(&master_pw).expect("Wrong password");

            unlocked_db.add(key.clone(), new_pw);
            unlocked_db.save(&file)?;

            println!("Added password for '{}'.", key);
            Ok(())
        }

        Commands::Delete { file, key } => {
            let master_pw = rpassword::prompt_password("Insert master password: ").unwrap();

            let db = PasswordManager::load(&file).expect("Failed to load database");
            let mut unlocked_db = db.unlock(&master_pw).expect("Wrong password");

            unlocked_db.delete(&key);
            unlocked_db.save(&file)?;

            println!("Deleted password for '{}'.", key);
            Ok(())
        }

        Commands::List { file, show } => {
            let db = PasswordManager::load(&file).expect("Failed to load database");

            if db.passwords.is_empty() {
                println!("No passwords stored.");
                return Ok(());
            }

            if show {
                // Path 1: User wants to see passwords.
                // We MUST prompt for the master password and transition to Unlocked.
                let master_pw = rpassword::prompt_password("Insert master password: ").unwrap();
                let unlocked_db = db.unlock(&master_pw).expect("Wrong password");

                for (k, v) in unlocked_db.list() {
                    println!("{}: {}", k, v);
                }
            } else {
                // Path 2: User only wants the keys.
                // We operate entirely on the `Locked` state! No master password required.
                for k in db.passwords.keys() {
                    println!("{}: ********", k);
                }
            }

            Ok(())
        }

        Commands::Count { file } => {
            // Notice how `Count` never calls `.unlock()`.
            // The compiler knows `count()` is available on `PasswordManager<Locked>`!
            let db = PasswordManager::load(&file).expect("Failed to load database");
            println!("Stored passwords: {}", db.count());
            Ok(())
        }
    }
}
