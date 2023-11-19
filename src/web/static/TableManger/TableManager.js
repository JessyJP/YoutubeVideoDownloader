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
        this.maxIdleChecks = 10;
        this.checkModeFlag = false;
        // Initialize the column handler
        this.columnManager = new ColumnManager(this.checkAndUpdateState.bind(this));
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
            await new Promise(resolve => setTimeout(resolve, 500)); // Wait for 500 ms
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
            const videoList = await getVideoItemList();
            this.populateTable(videoList);
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
                const row = this.videoListTableBody.insertRow();
                row.innerHTML = video.toTableRow(index, columnState);
            });
        }

        // Attach event listeners to all links
        const linksWatch = document.querySelectorAll('[data-watch-url]');
        // links.forEach(link => {  assignUrlClickListener(link)  });
        linksWatch.forEach(assignUrlClickListener);

        // Attach event listeners to all links
        const linksTitle = document.querySelectorAll('[data-title-url]');
        // linksTitle.forEach(link => {  assignTitleClickListener(link)  });
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
}

export default TableManager;