class ColumnManager {
    // ============= Initialization methods =============
    constructor(callbackOnVisibilityChange, postClientStateSettingsRef) {
        this.table = document.getElementById('video-list');
        this.contextMenu = document.getElementById('column-context-menu-id');
        this.columns = [];
        // External callback 
        this.onVisibilityChange = callbackOnVisibilityChange;
        this.postClientStateSettingsRef = postClientStateSettingsRef;
        // Initialize a default configuration
        this.defaultTableConfiguration();
        // TODO: this could be potentially overwritten here if on startup we load another configuration in the future
        this.initialize()
    }

    // Add new column
    addColumn(label, isVisible = true) {
        const columnIndex = this.columns.length;
        this.columns.push({ label, isVisible, id: `toggleColumn${columnIndex}` });
    }

    // Make a default configuration
    defaultTableConfiguration() {
        const labels = ['Index', 'Download Status', 'Watch URL', 'Title', 'Author', 'Length', 'Publish Date', 'Views', 'Thumbnail URL', 'Rating', 'Video ID', 'Quality', 'File Size (MB)'];
        labels.forEach(label => this.addColumn(label));
        // add 'Description' but set it to invisible by default
        this.addColumn('Description',false)
    }

    //This initializes the current configuration
    initialize() {
        this.populateTableHeaders();
        this.populateContextMenu();
        this.attachEventListeners();
    }

    populateTableHeaders() {
        const headerRow = this.table.createTHead().insertRow(0);
        this.columns.forEach((column, index) => {
            const th = document.createElement('th');
            th.textContent = column.label;
            if (!column.isVisible) {
                th.style.display = 'none';
            }
            headerRow.appendChild(th);
        });
    }

    populateContextMenu() {
        const menuItemsHTML = this.columns.map(column => 
            `<label><li><input type="checkbox" id="${column.id}" ${column.isVisible ? 'checked' : ''}> ${column.label}</li></label>`
        ).join('\n');
    
        this.contextMenu.innerHTML = `<ul>\n${menuItemsHTML}\n</ul>`;
    }
    

    attachEventListeners() {
        // Right-click event on table headers
        this.table.addEventListener('contextmenu', event => {
            event.preventDefault();
            if (event.target.tagName === 'TH') {
                this.contextMenu.style.display = 'block';
                this.contextMenu.style.left = `${event.pageX}px`;
                this.contextMenu.style.top = `${event.pageY}px`;

                // Update checkboxes based on column visibility
                this.columns.forEach((column, index) => {
                    const checkbox = document.getElementById(column.id);
                    if (checkbox) {
                        checkbox.checked = this.table.rows[0].cells[index].style.display !== 'none';
                    }
                });
            }
        });

        // Hide context menu on click outside
        window.addEventListener('click', () => {
            this.contextMenu.style.display = 'none';
        });

        // Checkbox change event in context menu
        this.columns.forEach((column, index) => {
            const checkbox = document.getElementById(column.id);
            if (checkbox) {
                checkbox.checked = column.isVisible;
                checkbox.addEventListener('change', () => {
                    this.setColumnVisibility(index, checkbox.checked);
                    // Also post the state when there is an update
                    this.postClientStateSettingsRef()
                });
            }
        });
    }

    // ============= Event handling methods =============

    setColumnVisibility(columnIndex, isVisible) {
        // Check if columnIndex is valid
        if (columnIndex < 0 || columnIndex >= this.columns.length) {
            console.error("Invalid column index");
            return;
        }
        
        if (this.columns[columnIndex].isVisible === isVisible) {
            return; // No change in visibility
        }
    
        Array.from(this.table.rows).forEach(row => {
            if (row.cells[columnIndex]) {
                row.cells[columnIndex].style.display = isVisible ? '' : 'none';
            }
        });
        this.columns[columnIndex].isVisible = isVisible;

        // Call the external callback if any
        if (this.onVisibilityChange) {
            this.onVisibilityChange();
        }
    }

    updateColumnOrder(newOrder) {//TODO:NOTE this method is currently inactive
        // newOrder is an array of column labels in the new order
        this.columns.sort((a, b) => newOrder.indexOf(a.label) - newOrder.indexOf(b.label));
        // Update the order property
        this.columns.forEach((column, index) => {
            column.order = index;
        });
    }

    // ============= Get/Set handling methods =============
    getVisibilityByLabel(label) {
        const column = this.columns.find(column => column.label === label);
        return column ? column.isVisible : null;
    }

    getAllColumnsVisibility() {
        return this.columns.map(column => ({
            label: column.label,
            isVisible: column.isVisible,
            order: column.order
        }));
    }

    updateColumnManagerState(data) {
        let newState;
    
        if (typeof data === 'string') {
            try {
                newState = JSON.parse(data);
            } catch (error) {
                console.error("Invalid JSON format");
                return;
            }
        } else if (typeof data === 'object' && Array.isArray(data)) {
            newState = data;
        } else {
            console.log("Error: Invalid data type, meaning the UI has not been given to the backend.");
            return;
        }
    
        newState.forEach(state => {
            const column = this.columns.find(column => column.label === state.label);
            if (column) {
                const columnIndex = this.columns.indexOf(column);
                // Compare current state with new state
                if (column.isVisible !== state.isVisible) {
                    this.setColumnVisibility(columnIndex, state.isVisible);
                }
            }
        });
    }
}


export default ColumnManager;