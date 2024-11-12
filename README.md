User: Has a one-to-many relationship with Order and a one-to-one relationship with Cart.
Product: Has relationships with Category, OrderItem, and CartItem.
Category: Linked to Product.
Order: Contains many OrderItems, has a relationship with User, and a one-to-one relationship with Payment.
OrderItem: Connects an Order and a Product.
Cart: Linked to User and has multiple CartItems.
CartItem: Connects a Cart and a Product.
Payment: Belongs to an Order and can be linked to a Sale.
Sale: Relates to a Payment.
Supplier: Has a one-to-many relationship with PurchaseOrder.
PurchaseOrder: Connects a Supplier to a Product.

1. Supplier Management
Supplier Model: Each supplier is represented by a record in the Supplier model, with fields like name, location, and distribution. These details help identify the suppliers and organize their information in the database.
Use Case: When creating a new supplier, the project can create a Supplier instance with information about the supplier's location, type of distribution (e.g., regional or national), and contact details. This enables easy retrieval and modification of supplier details when needed.
Supplier Listings: By querying the Supplier table, the application can display all available suppliers to the admin or warehouse staff, who can then manage or select suppliers for specific product restocking.


2. Purchase Orders
PurchaseOrder Model: This model tracks individual purchase orders placed with suppliers, including the quantity of products, the order_date, and the cost. It has foreign key references to both the Supplier and Product tables, connecting each order with the specific supplier providing it and the product being restocked.
Use Case: When inventory is running low on a particular product, the system can create a PurchaseOrder to restock. An entry in the PurchaseOrder table records this transaction, linking the order to the specific supplier and product.
Cost Management and Reporting: By storing cost in each purchase order, the system allows for tracking expenses on restocking and calculating inventory costs over time, which is valuable for financial reporting and budgeting.

3. Inventory and Order Fulfillment Integration
Inventory Management: The quantity field in PurchaseOrder and the association with Product help update the product stock upon receipt of goods from suppliers. Once a purchase order is fulfilled, the product's stock in the Product model could be incremented to reflect the new inventory level.
Supply Chain Efficiency: With a record of each purchase order and its associated supplier, the project can help administrators understand restocking times, evaluate supplier performance, and improve the procurement process by keeping track of historical data on suppliers and associated costs.

Example Workflow in the Project
Create Supplier: The admin adds suppliers into the system using the Supplier model.
Place a Purchase Order: When inventory is low, a new PurchaseOrder is created, linking to the relevant supplier and product, specifying the quantity and cost.
Inventory Update: Upon fulfillment of the purchase order, the project updates the Product stock to ensure that items are available for future customer orders.

