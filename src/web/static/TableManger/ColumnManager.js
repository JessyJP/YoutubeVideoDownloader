class ColumnManager {
    // ============= Initialization methods =============
    constructor() {
        this.table = document.getElementById('video-list');
        this.contextMenu = document.getElementById('contextMenu');
        this.columns = [];
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
        this.columns.forEach(column => {
            const th = document.createElement('th');
            th.textContent = column.label;
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
                    this.toggleColumnVisibility(index, checkbox.checked);
                });
            }
        });
    }

    // ============= Event handling methods =============

    toggleColumnVisibility(columnIndex, isVisible) {
        Array.from(this.table.rows).forEach(row => {
            if (row.cells[columnIndex]) {
                row.cells[columnIndex].style.display = isVisible ? '' : 'none';
            }
        });
        this.columns[columnIndex].isVisible = isVisible;
    }

    // ============= Get/Set handling methods =============

    getAllLabels() {
        return this.columns.map(column => column.label);
    }

    getVisibilityByLabel(label) {
        const column = this.columns.find(column => column.label === label);
        return column ? column.isVisible : null;
    }
}


export default ColumnManager;