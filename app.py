from flask import Flask, request, jsonify

from data.globals import ApiHttpConstants

app = Flask(__name__)

books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald", "is_borrowed": False},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee", "is_borrowed": False},
]

users = [
    {"id": 1, "name": "Alice", "borrowed_books": []},
    {"id": 2, "name": "Bob", "borrowed_books": []},
]

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books), ApiHttpConstants.OK

@app.route("/books", methods=["POST"])
def add_book():
    new_book = request.json
    if not new_book.get("title") or not new_book.get("author"):
        return jsonify({"error": "Missing required fields"}), ApiHttpConstants.BAD_REQUEST
    new_book["id"] = len(books) + 1
    new_book["is_borrowed"] = False
    books.append(new_book)
    return jsonify(new_book), ApiHttpConstants.CREATED

@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), ApiHttpConstants.NOT_FOUND
    data = request.json
    book.update(data)
    return jsonify(book), ApiHttpConstants.OK

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books
    book = next((b for b in books if b["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), ApiHttpConstants.NOT_FOUND
    books = [b for b in books if b["id"] != book_id]
    return jsonify({"message": "Book deleted"}), ApiHttpConstants.OK

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), ApiHttpConstants.OK

@app.route("/users/<int:user_id>/borrow/<int:book_id>", methods=["POST"])
def borrow_book(user_id, book_id):
    user = next((u for u in users if u["id"] == user_id), None)
    book = next((b for b in books if b["id"] == book_id), None)

    if not user:
        return jsonify({"error": "User not found"}), ApiHttpConstants.NOT_FOUND
    if not book:
        return jsonify({"error": "Book not found"}), ApiHttpConstants.NOT_FOUND
    if book["is_borrowed"]:
        return jsonify({"error": "Book already borrowed"}), ApiHttpConstants.BAD_REQUEST

    book["is_borrowed"] = True
    user["borrowed_books"].append(book_id)
    return jsonify({"message": "Book borrowed successfully"}), ApiHttpConstants.OK

@app.route("/users/<int:user_id>/return/<int:book_id>", methods=["POST"])
def return_book(user_id, book_id):
        user = next((u for u in users if u["id"] == user_id), None)
        book = next((b for b in books if b["id"] == book_id), None)

        if not user:
            return jsonify({"error": "User not found"}), ApiHttpConstants.NOT_FOUND
        if not book:
            return jsonify({"error": "Book not found"}), ApiHttpConstants.NOT_FOUND
        if book_id not in user["borrowed_books"]:
            return jsonify({"error": "Book was not borrowed by the user"}), ApiHttpConstants.BAD_REQUEST

        book["is_borrowed"] = False
        user["borrowed_books"].remove(book_id)
        return jsonify({"message": "Book returned successfully"}), ApiHttpConstants.OK

if __name__ == "__main__":
    app.run(debug=True)

