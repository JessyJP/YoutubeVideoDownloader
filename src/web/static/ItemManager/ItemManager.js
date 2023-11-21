import {
    getVideoItemList,
    getState,
    getStatusMsg,
    getProgressbarValue
} from '../api.js';
import { updateProgressBar } from "../functions.js"
import VideoItem from './VideoItem.js';

import ColumnManager from './ColumnManager.js';


class ItemManager {
    constructor() {
        // HTML Element handles
        this.videoListTableBody = document.getElementById('video-list').querySelector('tbody');
        this.gridContainer = document.getElementById('grid-container');
        this.statusOutput = document.getElementById('diagnostic-text'); // Assuming you have this element for status messages
        // Initialize the column handler/manager
        this.columnManager = new ColumnManager(this.checkAndUpdateState.bind(this));
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
        updateProgressBar(currentProgressValue)

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
            });
        } else if (this.viewMode === 'grid') {
            // Show grid and hide table
            document.getElementById('video-list').style.display = 'none';
            this.gridContainer.style.display = '';
    
            videoList.forEach((video, index) => {
                const gridElement = video.toGridCard(index, columnState);
                this.gridContainer.appendChild(gridElement);
            });

            this.adjustGridLayout();
        }
    }

    adjustGridLayout() {
        //TODO: if not going to be used externally just inline the method content
        this.gridContainer.style.gridTemplateColumns = `repeat(${this.maxGridCardsPerRow}, 1fr)`;
        this.gridContainer.style.gap = `var(--default-gap)`;
    }
    

    // When the server is performing processing, certain elements will be disabled in the UI
    setUIElementsByState(currentState) {
        // Example: disable/enable buttons based on the state
        const analyzeBtn = document.getElementById('analyze-btn'); 
        const downloadBtn = document.getElementById('download-btn'); 
        const clearItemsBtn = document.getElementById('clear-items-btn'); 
        // Similarly, get other buttons like 'set path'

        if (currentState === 'ANALYSIS') {
            analyzeBtn.disabled = true;
            downloadBtn.disabled = true;
            clearItemsBtn.disabled = true;
            // analyzeBtn.classList.add("disabled-button");
            // downloadBtn.classList.add("disabled-button");
            // Set other buttons as needed
        } else if (currentState === 'DOWNLOAD') {
            analyzeBtn.disabled = true;
            downloadBtn.disabled = true;
            clearItemsBtn.disabled = true;
            // analyzeBtn.classList.add("disabled-button");
            // downloadBtn.classList.add("disabled-button");
            // Set other buttons as needed
        } else {
            analyzeBtn.disabled = false;
            downloadBtn.disabled = false;
            clearItemsBtn.disabled = false;
            // analyzeBtn.classList.remove("disabled-button");
            // downloadBtn.classList.remove("disabled-button");
            // Set other buttons as needed
        }
    }

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

}

export default ItemManager;