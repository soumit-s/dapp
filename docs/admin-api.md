# Routes
```py
GET /api/v1/admin/profile
PUT /api/v1/admin/profile

GET /api/v1/admin/stores # Get all stores.
GET /api/v1/admin/stores/:id # Get details of a specific store.
POST /api/v1/admin/stores # Creates a new store
POST /api/v1/admin/stores/search # Semantic search over stores.
PUT /api/v1/admin/stores/:id # Replaces existing store, NOTE: does not change status
PATCH /api/v1/admin/stores/:id/status

GET /api/v1/admin/products?page=<int>&limit=<int>&sort_by=<created_at, name>&order=<asc, desc>
GET /api/v1/admin/products/:id # Get details of a specific product
POST /api/v1/admin/products # Creates a new product
POST /api/v1/admin/products/search # Semantic search over product
PUT /api/v1/admin/products/:id # Replaces existing product

GET /api/v1/admin/stores/:store_id/inventory?page=<int>&limit=<int>
GET /api/v1/admin/stores/:store_id/inventory/:product_id

# Creates new item
POST /api/v1/admin/stores/:store_id/inventory

POST /api/v1/admin/stores/:store_id/inventory/search # Semantic search on a specific store inventory.
PATCH /api/v1/admin/stores/:store_id/inventory/:product_id/adjust
PATCH /api/v1/admin/stores/:store_id/inventory/:product_id/status
```


# Get stores API
Route: /api/v1/admin/stores

#### Response
```js
type Response = {
    stores: {
        id: number, // integer
        name: string,
        description: string,
        lat: number,
        long: number,
        is_active: boolean,
    }[]
}
```

# Get products API
Route: /api/v1/admin/products
#### Response
```js
type Response = {
    products: {}
}
```