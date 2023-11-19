import {
    getVideoItemList,
    getState,
    getStatusMsg,
    getProgressbarValue
} from '../api.js';
import { updateProgressBar } from "../functions.js"
import {
     VideoItem, 
     assignUrlClickListener, 
     assignTitleClickListener 
    } from "./VideoItem.js";

import ColumnManager from './ColumnManager.js';


class TableManager {
    constructor() {
        this.videoListTableBody = document.getElementById('video-list').querySelector('tbody');
        this.statusOutput = document.getElementById('diagnostic-text'); // Assuming you have this element for status messages
        this.updateInterval = null;
        // The auto-update parameters
        this.idleCheckCounter = 0;
        this.maxIdleChecks = 12;
        this.refreshTimeout = 250;//ms
        this.checkModeFlag = false;
        this.viewMode = 'table'; // Default view mode
        // Initialize the column handler
        this.columnManager = new ColumnManager(this.checkAndUpdateState.bind(this));
        // Store temp states
        this.videoItems = [];
        this.selection  = [];
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
            await new Promise(resolve => setTimeout(resolve, this.refreshTimeout)); // Wait for this.refreshTimeout ms
        }
    }

    resetIdleCheckCounter() {
        this.idleCheckCounter = 0;
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
            // videoList = this.transferSelectionFromDom(videoList)
            this.populateTable(videoList);
            // Store the video list after transferring the selection
            this.videoItems = videoList
        } catch (error) {
            console.error("Error fetching video list: ", error);
        }
    }

    populateTable(videoList) {
        const columnState = this.columnManager.getColumnState();
        this.videoListTableBody.innerHTML = ''; // Clear existing rows
    
        if (videoList.length === 0) {
            const row = this.videoListTableBody.insertRow();
            row.innerHTML = `<td colspan="15" style="text-align:center;">No videos found</td>`;
        } else {
            videoList.forEach((video, index) => {
                const rowElement = video.toTableRow(index, columnState);
                this.videoListTableBody.appendChild(rowElement); // Append the row element directly
            });
        }
    
        // Attach event listeners to all links
        const linksWatch = this.videoListTableBody.querySelectorAll('[data-watch-url]');
        linksWatch.forEach(assignUrlClickListener);
    
        const linksTitle = this.videoListTableBody.querySelectorAll('[data-title-url]');
        linksTitle.forEach(assignTitleClickListener);
    }

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
    //NOTE:TODO: one of the 2 methods will be redundant
    transferSelectionFromDom(videoListTo) {
        // Check if this.videoItems is undefined or empty
        if (!this.videoItems || this.videoItems.length === 0) {
            return videoListTo;
        }
    
        // Loop over the videoListTo array
        videoListTo.forEach(toItem => {
            // Find the corresponding item in this.videoItems array
            const fromItem = this.videoItems.find(item => item.video_id === toItem.video_id);
    
            // If a matching item is found, transfer the selection state
            if (fromItem) {
                toItem.itemIsSelected = fromItem.itemIsSelected;
            }
        });
    
        return videoListTo;
    }
    

}

export default TableManager;