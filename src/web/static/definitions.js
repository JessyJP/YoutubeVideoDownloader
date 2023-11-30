// For import in the API
export const API_PROXY = "http://localhost:8080"; // Replace with your actual IP and port.

// Define the environment state for production or development
export const is_production_environment = true; 

// For import in the Item Manager
export const refreshTimeoutFactor = 100; // Default interval between refreshes in ms when IDLE
export const maxIdleChecks = 4+1; // Default maximum number of refreshes when server in IDLE 
export const viewMode = 'table'; // Default view mode
export const maxGridCardsPerRow = 2; // Default Maximum number of grid cards per row

// For import into the Column manager
// The default column menu visibility
export const defaultTableColumnConfiguration = [
    { label: 'Index', visible: true },
    { label: 'Download Status', visible: true },
    { label: 'Watch URL', visible: true },
    { label: 'Title', visible: true },
    { label: 'Author', visible: true },
    { label: 'Length', visible: true },
    { label: 'Publish Date', visible: true },
    { label: 'Views', visible: true },
    { label: 'Thumbnail URL', visible: true },
    { label: 'Rating', visible: true },
    { label: 'Video ID', visible: true },
    { label: 'Quality', visible: true },
    { label: 'File Size (MB)', visible: true },
    { label: 'Description', visible: false } // 'Description' is set to invisible by default
  ];

  export const resetTheAnalysisInputBar = true;