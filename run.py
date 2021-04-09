from web_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True) # debug true means that it autoreloads config
