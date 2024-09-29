Tic Tech Toe 24

Team : Code Blunders

A structured approach to building an e-library system involves creating a homepage that is accessible to all users without requiring login or signup. Users can browse available books or materials but are prompted to log in before downloading. Upon login, users can upload documents, access public materials, and request access to private documents shared by other users.

To manage user data and file operations, three distinct database models are employed. Elasticsearch powers the search functionality, enabling quick and accurate searches based on user input. Celery is integrated to handle asynchronous tasks like sending OTPs and notifications, ensuring smooth user experience.

For the recommendation system, a hybrid approach is used, leveraging Matrix Factorization for user feedback and ratings, and TF-IDF with Cosine Similarity for content-based recommendations based on book attributes.

