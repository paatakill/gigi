from ext import app

if __name__ == "__main__":
    from routes import home, registration, authorization, profile, comment, review, review_page, delete_review, edit_review, contact, delete_comment
    app.run(debug=True)

