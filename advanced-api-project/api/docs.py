"""
API Documentation for Advanced Book API

CORRECTED View Configurations and Custom Behavior:

Django REST Framework Generic View Classes Used:

1. ListAPIView - For listing multiple objects
   - BookListView (GET /api/books/)
   - AuthorListView (GET /api/authors/)

2. RetrieveAPIView - For retrieving single objects  
   - BookDetailView (GET /api/books/<id>/)
   - AuthorDetailView (GET /api/authors/<id>/)

3. CreateAPIView - For creating new objects
   - BookCreateView (POST /api/books/create/)
   - AuthorCreateView (POST /api/authors/create/)

4. UpdateAPIView - For updating existing objects
   - BookUpdateView (PUT/PATCH /api/books/<id>/update/)
   - AuthorUpdateView (PUT/PATCH /api/authors/<id>/update/)

5. DestroyAPIView - For deleting objects
   - BookDeleteView (DELETE /api/books/<id>/delete/)
   - AuthorDeleteView (DELETE /api/authors/<id>/delete/)

6. RetrieveUpdateDestroyAPIView - Combined operations
   - BookRetrieveUpdateDeleteView (GET/PUT/PATCH/DELETE /api/books/<id>/manage/)
   - AuthorRetrieveUpdateDeleteView (GET/PUT/PATCH/DELETE /api/authors/<id>/manage/)

Key Differences from Incorrect Naming:
- ListAPIView (NOT ListView)
- RetrieveAPIView (NOT DetailView) 
- CreateAPIView (NOT CreateView)
- UpdateAPIView (NOT UpdateView)
- DestroyAPIView (NOT DeleteView)
- RetrieveUpdateDestroyAPIView (Combined view)

URL Patterns Structure:
- List views: /api/books/ (GET)
- Create views: /api/books/create/ (POST) 
- Detail/Retrieve views: /api/books/<id>/ (GET)
- Update views: /api/books/<id>/update/ (PUT/PATCH)
- Delete views: /api/books/<id>/delete/ (DELETE)
- Combined views: /api/books/<id>/manage/ (GET/PUT/PATCH/DELETE)
"""