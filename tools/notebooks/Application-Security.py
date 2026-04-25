import marimo

__generated_with = "0.13.11"
app = marimo.App(width="medium", app_title="DTLab - ApplicationSecurity")


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        f"""
    # Hashing
    Hashing is a one-way encryption. Different ways to perform hashing

    * Unsecure, non cryptographic: MD4, MD5\n
    * Secure, non cryptographic: SHA-1, SHA-2, SHA-3\n
    * Secure, cryptographic: bcrypt, argon2\n

    ## Setup
    To run the shell command, use your Kali Linux virtual machine.

    There is already a rockyou wordlist in kali, but you need to decompress it:
    ```sh
    sudo gunzip /usr/share/wordlists/rockyou.tar.gz
    ```
    Or you can download a local copy from the link below:

    ```sh
    curl -fL -O https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt
    ```

    A useful command to know how an hash was generated
    ```sh
    hash-identifier <hash>
    ```
    """
    )
    return


@app.cell(hide_code=True)
def _(argon2, mo, platform):
    password = mo.ui.text(placeholder="Password")

    md = None
    if platform.machine() != "wasm32":
        time_cost = mo.ui.slider(1, argon2.DEFAULT_TIME_COST * 2, value=argon2.DEFAULT_TIME_COST)
        parallelism = mo.ui.slider(1, argon2.DEFAULT_PARALLELISM * 2, value=argon2.DEFAULT_PARALLELISM)
        hash_len = mo.ui.slider(8, argon2.DEFAULT_HASH_LENGTH* 2, value=argon2.DEFAULT_HASH_LENGTH)
        salt_len = mo.ui.slider(8, argon2.DEFAULT_RANDOM_SALT_LENGTH* 2, value=argon2.DEFAULT_RANDOM_SALT_LENGTH)
        memory_cost = mo.ui.slider(1, argon2.DEFAULT_MEMORY_COST* 2, value=argon2.DEFAULT_MEMORY_COST)

        md = mo.md(f"""
        ## Insert your passsword here: {password}

        ### Argon2 hash parameters
        Play with these values and see how the argon2 hash changes.

        Time cost: {time_cost} \n
        Parallelism: {parallelism}\n
        Hash Length: {hash_len}\n
        Salt Length: {salt_len}\n
        Memory cost: {memory_cost}\n
        """)
    else: 
        md = mo.md(f"""
        ## Insert your passsword here: {password}
        """)
    md
    return hash_len, memory_cost, parallelism, password, salt_len, time_cost


@app.cell(hide_code=True)
def _(
    argon2,
    bcrypt,
    hash_len,
    hashlib,
    memory_cost,
    mo,
    parallelism,
    password,
    platform,
    salt_len,
    time_cost,
):
    plaintext = password.value.encode()

    # md5
    md5 = hashlib.md5(plaintext)

    # sha256
    sha256 = hashlib.sha256(plaintext)

    # bcrypt
    bcrypt_salt = bcrypt.gensalt()
    bcrypt_hash = bcrypt.hashpw(plaintext, bcrypt_salt)

    if platform.machine() != "wasm32":
        # argon2
        argon2_hash = argon2.PasswordHasher(
            time_cost=time_cost.value,
            memory_cost=memory_cost.value,
            parallelism=parallelism.value,
            salt_len=salt_len.value,
            hash_len=hash_len.value
        ).hash(plaintext)

    mo.md(f"""
    ### Argon2
    Hash: {'argon2 not supported' if platform.machine() == 'wasm32' else argon2_hash}

    ### Bcrypt
    Salt: {bcrypt_salt}

    Hash: {bcrypt_hash}

    ### MD5
    Not secure. Crackable with hashcat or john the ripper. Detect hash type with
    ```sh
    hash-identifier { md5.hexdigest() }
    ```

    ```sh
    hashcat -m0 hash.txt rockyou.txt
    ```
    ```sh
    john -format=raw-md5 --wordlist=rockyou.txt hash.txt
    ```

    ## SHA
    Secure Hash Algorithm (SHA) is a group of algorithm used instead to verify integrity of files for security reason. Detect hash-type with:
    ```sh
    hash-identifier { sha256.hexdigest() }
    ```

    ```sh
    john -format=raw-sha256 --wordlist /usr/share/wordlists/rockyou.txt  hash.txt
    ```
    """)
    return


@app.cell
def _(mo, pd):
    df_test = pd.read_json(
        "https://raw.githubusercontent.com/vega/vega-datasets/master/data/cars.json"
    )

    mo.md(
        f"""
        # SQL Intro
        Structured Query Language used to interact with a database. Very easy and prone to **injection**.

        Let's create a dummy database.
        """
    )

    #mo.ui.dataframe(df_test)
    return (df_test,)


@app.cell
def _(df_test, mo):
    _df = mo.sql(
        f"""
        SELECT * FROM df_test
        """
    )
    return


@app.cell
def _(contextlib, sqlite3):
    with contextlib.closing(sqlite3.connect("tutorial.db")) as conn:
        with conn as cur:
            cur.execute("CREATE TABLE IF NOT EXISTS users(id, username, password)")

        with conn as cur:
            cur.execute("DELETE FROM users")
            cur.execute(f"""INSERT INTO users (id, username, password) 
            VALUES
            (1, 'giuseppe', 'password'),
            (2, 'simone', 'test123'),
            (3, 'gaia', 'test123')

            """)

        with conn as cur:
            data = cur.execute("SELECT * FROM users")
            print(data.fetchall())
    return


@app.cell
def _(contextlib, mo, sqlite3):
    def handle_login(value) -> None:
        global result
        query = f"SELECT * from users where username = '{username_field.value}' AND users.password='{password_field.value}'"
        print(query)
        with contextlib.closing(sqlite3.connect("tutorial.db")) as conn:
            with conn as cur:
                data = cur.execute(query).fetchone()
                result = data if data is not None else "User not found"
                print(result)


    username_field = mo.ui.text(placeholder="Username")
    password_field = mo.ui.text(placeholder="Password", kind="password")
    login_button = mo.ui.button(on_click=handle_login, label="Login")

    mo.md(f"""
    ### A simple form
    Username: {username_field}
    Password: {password_field}

    {login_button}
    """)
    return password_field, username_field


@app.cell
def _(bcrypt, contextlib, sqlite3):
    with contextlib.closing(sqlite3.connect("tutorial.db")) as con:
        with con as c:
            users = c.execute("SELECT * FROM users")
            for user in users:
                hash = bcrypt.hashpw(user[2].encode(), bcrypt.gensalt())
                c.execute(f"UPDATE users set password = '{hash}' WHERE id = {user[0]}")

        with con as c:
            users = c.execute("SELECT * FROM users")
            print(users.fetchall())
    return


@app.cell
def _(bcrypt, contextlib, mo, password_field, sqlite3, username_field):
    def better_login(ctx) -> None:
        query = f"SELECT * from users where username = '{username_field.value}'"
        print(query)
        with contextlib.closing(sqlite3.connect("tutorial.db")) as conn:
            with conn as cur:
                user = cur.execute(query).fetchone()
                if bcrypt.checkpw(password_field.value.encode(), user[2].encode()):
                    print("Success", user)
                else:
                    print("bad user")

    better_button = mo.ui.button(on_click=better_login, label="Login")

    mo.md(f"""
    ### A simple form (improved)
    Username: {username_field}
    Password: {password_field}

    {better_button}
    """)
    return


@app.cell
def _():
    import hashlib
    import pandas as pd
    import sqlite3
    import contextlib
    return contextlib, hashlib, pd, sqlite3


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
