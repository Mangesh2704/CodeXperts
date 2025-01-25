// Mock Inventory Data
let inventory = [];
let isEditing = false; // Flag to track editing state
let editItemId = null; // ID of the item being edited

// Function to render inventory in the table
function renderInventory() {
  const inventoryTable = document.getElementById('inventoryTable');
  inventoryTable.innerHTML = ''; // Clear the table

  // Reassign dynamic IDs to maintain sequential order
  inventory.forEach((item, index) => {
    item.id = index + 1; // Dynamically assign IDs
  });

  // Render the inventory table
  inventory.forEach(item => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${item.id}</td>
      <td>${item.name}</td>
      <td>${item.quantity}</td>
      <td>${item.entryDate}</td>
      <td>${item.expiryDate}</td>
      <td>
        <button class="view" onclick="viewItem(${item.id})">View</button>
        <button class="update" onclick="startEditItem(${item.id})">Update</button>
        <button class="delete" onclick="deleteItem(${item.id})">Delete</button>
      </td>
    `;
    inventoryTable.appendChild(row);
  });
}

// Add or Update Item
document.getElementById('addButton').addEventListener('click', () => {
  const itemName = document.getElementById('itemName').value;
  const itemQuantity = document.getElementById('itemQuantity').value;
  const entryDate = document.getElementById('entryDate').value;
  const expiryDate = document.getElementById('expiryDate').value;

  // Validate form inputs
  if (
    itemName.trim() === '' || 
    itemQuantity.trim() === '' || 
    entryDate.trim() === '' || 
    expiryDate.trim() === ''
  ) {
    alert('Please fill out all fields.');
    return;
  }

  if (Number(itemQuantity) < 0) {
    alert('Quantity cannot be negative.');
    return;
  }
  if (Number(itemQuantity) == 0) {
    alert('Quantity cannot be zero.');
    return;
  }

  // Validate that expiry date is not before entry date
  if (new Date(expiryDate) < new Date(entryDate)) {
    alert('Expiry date cannot be earlier than entry date.');
    return;
  }

  if (isEditing) {
    // Update existing item
    const item = inventory.find(item => item.id === editItemId);
    if (item) {
      item.name = itemName;
      item.quantity = itemQuantity;
      item.entryDate = entryDate;
      item.expiryDate = expiryDate;
      alert('Item updated successfully!');
    }
    // Reset editing state
    isEditing = false;
    editItemId = null;
    document.getElementById('addButton').textContent = 'Add Item';
  } else {
    // Add new item
    inventory.push({
      id: inventory.length + 1, // Assign the next sequential ID
      name: itemName,
      quantity: itemQuantity,
      entryDate,
      expiryDate,
    });
    alert('Item added successfully!');
  }

  renderInventory();
  clearInputs();
});

// Start Editing Item
function startEditItem(id) {
  const item = inventory.find(item => item.id === id);
  if (!item) {
    alert('Item not found.');
    return;
  }

  // Pre-fill the input fields with the current item data
  document.getElementById('itemName').value = item.name;
  document.getElementById('itemQuantity').value = item.quantity;
  document.getElementById('entryDate').value = item.entryDate;
  document.getElementById('expiryDate').value = item.expiryDate;

  // Change the "Add" button to "Update"
  document.getElementById('addButton').textContent = 'Update Item';
  isEditing = true;
  editItemId = id;
}

// View Item Details
function viewItem(id) {
  const item = inventory.find(item => item.id === id);
  if (item) {
    alert(`
      Item Name: ${item.name}
      Quantity: ${item.quantity}
      Entry Date: ${item.entryDate}
      Expiry Date: ${item.expiryDate}
    `);
  } else {
    alert('Item not found.');
  }
}

// Delete Item
function deleteItem(id) {
  // Filter out the item to be deleted
  inventory = inventory.filter(item => item.id !== id);

  // Re-render inventory and dynamically reassign IDs
  renderInventory();
}

// Clear Input Fields
function clearInputs() {
  document.getElementById('itemName').value = '';
  document.getElementById('itemQuantity').value = '';
  document.getElementById('entryDate').value = '';
  document.getElementById('expiryDate').value = '';
}

// Initial Render
renderInventory();
