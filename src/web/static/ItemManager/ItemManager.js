import {
    getVideoItemList,
    getState,
    getStatusMsg,
    getProgressbarValue,
    postClientStateSettings,
    changeStatusForItemsSelectedByID
} from '../api.js';
import { updateProgressBarUi } from "../functions.js"
import VideoItem from './VideoItem.js';

import ColumnManager from './ColumnManager.js';


class ItemManager {
    constructor() {
        // HTML Element handles
        this.videoListTableBody = document.getElementById('video-list').querySelector('tbody');
        this.gridContainer = document.getElementById('grid-container');
        this.statusOutput = document.getElementById('diagnostic-text'); // Assuming you have this element for status messages
        // Elements for state control
        this.analyzeBtn = document.getElementById('analyze-btn'); 
        this.downloadBtn = document.getElementById('download-btn'); 
        // Initialize the column handler/manager
        this.columnManager = new ColumnManager(this.checkAndUpdateState.bind(this), postClientStateSettings.bind(null, this));
        // Video items storing array for
        this.videoItems = [];
        // The auto-update internal variables
        this.checkModeFlag = false;
        this.idleCheckCounter = 0;
        // The auto-update parameters
        this.refreshTimeoutFactor = 50;// Default interval between refreshes ms in IDLE
        this.maxIdleChecks = 12;// Default maximum number of refreshes when server in IDLE 
        this.viewMode = 'table'; // Default view mode
        this.maxGridCardsPerRow = 2; // Default Maximum number of grid cards per row

        // Attach the container event listeners only once
        this.attachContextMenuListener()
    }

    async checkAndUpdateState() {
        if (this.checkModeFlag) {
            return; // Already in check mode, so exit early
        }
        this.checkModeFlag = true;

        while (this.checkModeFlag) {
            const currentState = await getState();
            if (currentState === 'IDLE') {
                this.idleCheckCounter++;
                if (this.idleCheckCounter >= this.maxIdleChecks) {
                    this.checkModeFlag = false; // Exit check mode
                    this.resetIdleCheckCounter();
                    break;
                }
            } else {
                this.resetIdleCheckCounter();
            }

            this.updateUI();
            await this.delay(this.refreshTimeoutFactor*this.idleCheckCounter); // Update a few times with increasing delay
        }
    }

    resetIdleCheckCounter() {
        this.idleCheckCounter = 0;
    }

    async delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async updateUI() {
        const currentState = await getState();
        const currentStatusMsg = await getStatusMsg();
        const currentProgressValue = await getProgressbarValue()

        // Update status text and UI elements based on the current state
        this.setUIElementsByState(currentState);
        this.statusOutput.textContent = currentStatusMsg;
        updateProgressBarUi(currentProgressValue)

        // Update the video list table 
        try {
            let videoList = await getVideoItemList();
            videoList = this.transferSelection(this.videoItems, videoList)
            // Display the items which populates the display container
            this.displayItems(videoList);
            // Store the video list after transferring the selection
            this.videoItems = videoList
        } catch (error) {
            console.error("Error fetching video list: ", error);
        }
    }

    displayItems(videoList) {
        const columnState = this.columnManager.getAllColumnsVisibility();
    
        // Clear existing rows for table view
        this.videoListTableBody.innerHTML = ''; 
        // Clear existing grid elements
        this.gridContainer.innerHTML = ''; 
    
        if (videoList.length === 0) {
            const row = this.videoListTableBody.insertRow();
            row.innerHTML = `<td colspan="15" style="text-align:center;">No videos found</td>`;
            return;
        }

        if (this.viewMode === 'table') {
            // Show table and hide grid
            document.getElementById('video-list').style.display = '';
            this.gridContainer.style.display = 'none';
    
            videoList.forEach((video, index) => {
                const rowElement = video.toTableRow(index, columnState);
                this.videoListTableBody.appendChild(rowElement);
                // video.setSelectionStateAndUpdateUI(video.itemIsSelected)
            });
        } else if (this.viewMode === 'grid') {
            // Show grid and hide table
            document.getElementById('video-list').style.display = 'none';
            this.gridContainer.style.display = '';
    
            videoList.forEach((video, index) => {
                const gridElement = video.toGridCard(index, columnState);
                this.gridContainer.appendChild(gridElement);
                video.setSelectionStateAndUpdateUI(video.itemIsSelected)
            });

            this.adjustGridLayout(this.maxGridCardsPerRow);
        }
    }

    adjustGridLayout(maxGridCardsPerRow) {
        this.gridContainer.style.gridTemplateColumns = `repeat(${maxGridCardsPerRow}, 1fr)`;
        this.gridContainer.style.gap = `var(--default-gap)`;
        this.maxGridCardsPerRow = maxGridCardsPerRow;
    }
    

    // When the server is performing processing, certain elements will be disabled in the UI
    setUIElementsByState(currentState) {        
        if (currentState === 'ANALYSIS') {
            this.analyzeBtn.disabled = true;
            this.downloadBtn.disabled = true;
            // this.analyzeBtn.classList.add("disabled-button");
            // this.downloadBtn.classList.add("disabled-button");
            // Set other buttons as needed
        } else if (currentState === 'DOWNLOAD') {
            this.analyzeBtn.disabled = true;
            this.downloadBtn.disabled = true;
            // this.analyzeBtn.classList.add("disabled-button");
            // this.downloadBtn.classList.add("disabled-button");
            // Set other buttons as needed
        } else {
            this.analyzeBtn.disabled = false;
            this.downloadBtn.disabled = false;
            // this.analyzeBtn.classList.remove("disabled-button");
            // this.downloadBtn.classList.remove("disabled-button");
            // Set other buttons as needed
        }
    }

    // ================================ Methods for handling the selection ================================

    transferSelection(videoListFrom, videoListTo) {
        // Check if videoListFrom is undefined or empty
        if (!videoListFrom || videoListFrom.length === 0) {
            return videoListTo;
        }
    
        // Loop over the videoListTo array
        videoListTo.forEach(toItem => {
            // Find the corresponding item in the videoListFrom array
            const fromItem = videoListFrom.find(item => item.video_id === toItem.video_id);
    
            // If a matching item is found, transfer the selection state
            if (fromItem) {
                toItem.itemIsSelected = fromItem.itemIsSelected;
            }
        });
    
        return videoListTo;
    }

    setAllItemsAsSelected(){
        this.videoItems.forEach(item => {
            item.setSelectionStateAndUpdateUI(true);
        })
    }

    setAllItemsAsDeselected(){
        this.videoItems.forEach(item => {
            item.setSelectionStateAndUpdateUI(false);
        })
    }

    // Get functions for the item selections
    getSelectedItems() {
        return this.videoItems.filter(item => item.itemIsSelected);
    }

    getSelectedItemIds() {
        return this.getSelectedItems().map(item => item.video_id);
    }

     // ========================== Methods for handling the video items context menu ==========================
    attachContextMenuListener() {
        // Attach to both the table body and grid container
        this.videoListTableBody.addEventListener('contextmenu', this.handleContextMenu.bind(this));
        this.gridContainer.addEventListener('contextmenu', this.handleContextMenu.bind(this));

        // Hide context menu when clicking outside
        document.addEventListener('click', (event) => {
            const existingMenu = document.querySelector('.toggle-context-popup');
            if (existingMenu && !existingMenu.contains(event.target)) {
                existingMenu.remove();
            }
        });
    }

    async handleContextMenu(event) {
        event.preventDefault();

        // Remove any existing context menu
        const existingMenu = document.querySelector('.toggle-context-popup');
        if (existingMenu) existingMenu.remove();

        const popupMenu = await this.createContextMenu();
        popupMenu.style.top = `${event.pageY}px`;
        popupMenu.style.left = `${event.pageX}px`;

        document.body.appendChild(popupMenu);
    }

    handleMenuItemClick(statusToggle) {
        console.log(`Change download status to: ${statusToggle}`);
        // Handle the click event on a menu item
        const selectedItems = this.getSelectedItemIds();

        changeStatusForItemsSelectedByID(statusToggle,selectedItems)

        // Use API calls to send updates to the server
        console.log("Menu item toggle [",statusToggle,"] clicked with selected items:", selectedItems);

        // Remove any existing context menu
        const existingMenu = document.querySelector('.toggle-context-popup');
        if (existingMenu) existingMenu.remove();

        this.checkAndUpdateState()
    }

    async createContextMenu() {
        const selectedItems = this.getSelectedItems();
        const selectedItemsCount = selectedItems.length;
        const currentState = await getState();
        const isProcessActive = currentState !== "IDLE";
    
        // The popup menu HTML element
        const popupMenu = document.createElement('div');
        popupMenu.className = 'toggle-context-popup';
    
        // Show the item count
        const countItem = document.createElement('div');
        countItem.textContent = `${selectedItemsCount} item(s) selected`;
        countItem.id = 'toggle-context-popup-item-selection-count';
        countItem.className = 'toggle-context-popup-item disabled';
        popupMenu.appendChild(countItem);
    
        // Define the Menu items including separators
        const menuItems = [
            { label: 'Download Status: Pending', action: () => this.handleMenuItemClick('pending'), disabled: isProcessActive },
            { label: 'Download Status: Skip', action: () => this.handleMenuItemClick('skip'), disabled: isProcessActive },
            { type: 'separator' },
            { label: 'Keep Audio Only: Toggle Add/Remove', action: () => this.handleMenuItemClick('audio'), disabled: isProcessActive },
            { label: 'Keep Video Only: Toggle Add/Remove', action: () => this.handleMenuItemClick('video'), disabled: isProcessActive },
            { label: 'Keep All Subtitles Only: Toggle Add/Remove', action: () => this.handleMenuItemClick('subtitles'), disabled: isProcessActive },
            { label: 'Keep Thumbnail:   Toggle Add/Remove', action: () => this.handleMenuItemClick('thumbnail'), disabled: isProcessActive },
            { label: 'Keep Info:       Toggle Add/Remove', action: () => this.handleMenuItemClick('info'), disabled: isProcessActive },
            { label: 'Keep Comments:   Toggle Add/Remove', action: () => this.handleMenuItemClick('comments'), disabled: isProcessActive },
            { label: 'Clear All Keeps', action: () => this.handleMenuItemClick('clear'), disabled: isProcessActive },
            { type: 'separator' },
            { label: 'Remove Selected Entries', action: () => this.handleMenuItemClick('remove'), disabled: isProcessActive },

        ];
        
        // Add the menu items
        menuItems.forEach(item => {
            if (item.type === 'separator') {
                const separator = document.createElement('div');
                separator.className = 'toggle-context-popup-separator';
                popupMenu.appendChild(separator);
            } else {
                const menuItem = document.createElement('div');
                menuItem.textContent = item.label;
                menuItem.className = 'toggle-context-popup-item';
                if (!item.disabled) {
                    menuItem.addEventListener("click", () => item.action(selectedItems));
                } else {
                    menuItem.classList.add("disabled");
                }
                popupMenu.appendChild(menuItem);
            }
        });
    
        return popupMenu;
    }
}

export default ItemManager;