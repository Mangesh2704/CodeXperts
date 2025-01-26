// Mock Inventory Data
let inventory = JSON.parse(localStorage.getItem('inventory')) || []; // Load from localStorage
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

  // Save updated inventory to localStorage
  localStorage.setItem('inventory', JSON.stringify(inventory));

  // Render the inventory table
  inventory.forEach(item => {
    const row = document.createElement('tr');

    // Calculate remaining days to expiry
    const today = new Date();
    const expiryDate = new Date(item.expiryDate);
    const daysLeft = Math.ceil((expiryDate - today) / (1000 * 60 * 60 * 24));

    // Add a class if expiry is within 2 days
    if (daysLeft <= 2) {
      row.classList.add('expiring-soon');
    }

    row.innerHTML = `
      <td>${item.id}</td>
      <td>${item.name}</td>
      <td>${item.quantity}</td>
      <td>${item.entryDate}</td>
      <td>${item.expiryDate}</td>
      <td>
        <button class="view" onclick="viewItem(${item.id})">View</button>
        <button class="update" onclick="startEditItem(${item.id})">Update</button>
        <button id = "delete" class="delete" onclick="deleteItem(${item.id})">Delete</button>
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

// Load inventory from localStorage on page load
window.onload = renderInventory;


