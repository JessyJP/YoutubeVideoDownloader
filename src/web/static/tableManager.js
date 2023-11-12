import {
    getVideoItemList,
    getState,
    getStatusMsg
} from './api.js';

class TableManager {
    constructor() {
        this.videoListTableBody = document.getElementById('video-list').querySelector('tbody');
        this.statusOutput = document.getElementById('diagnostic-text'); // Assuming you have this element for status messages
        this.updateInterval = null;
        // The auto-update parameters
        this.idleCheckCounter = 0;
        this.maxIdleChecks = 10;
        this.checkModeFlag = false;
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
        
        // Update status text and UI elements based on the current state
        this.setUIElementsByState(currentState);
        this.statusOutput.textContent = currentStatusMsg;

        // Update the video list table 
        try {
            const videoList = await getVideoItemList();
            this.populateTable(videoList);
        } catch (error) {
            console.error("Error fetching video list: ", error);
        }
    }

    populateTable(videoList) {
        this.videoListTableBody.innerHTML = ''; // Clear existing rows

        if (videoList.length === 0) {
            const row = this.videoListTableBody.insertRow();
            row.innerHTML = `<td colspan="15" style="text-align:center;">No videos found</td>`;
        } else {
            videoList.forEach((video, index) => {
                const row = this.videoListTableBody.insertRow();
                row.innerHTML = `
                    <td>${index + 1}</td>
                    <td>${video.download_status || 'N/A'}</td>
                    <td>${video.watch_url}</td>
                    <td>${video.title || 'N/A'}</td>
                    <td>${video.author || 'N/A'}</td>
                    <td>${video.length != null ? video.length : 'N/A'}</td>
                    <td>${video.description || 'N/A'}</td>
                    <td>${video.publish_date || 'N/A'}</td>
                    <td>${video.views != null ? video.views : 'N/A'}</td>
                    <td>${video.thumbnail_url || 'N/A'}</td>
                    <td>${video.rating || 'N/A'}</td>
                    <td>${video.video_id || 'N/A'}</td>
                    <td>${video.quality_str || 'N/A'}</td>
                    <td>${video.video_size_mb || 'N/A'}</td>
                `;
            });
        }
    }


    setUIElementsByState(currentState) {
        // Example: disable/enable buttons based on the state
        const analyzeBtn = document.getElementById('analyze-btn'); // Assuming this is your analyze button
        const downloadBtn = document.getElementById('download-btn'); // Assuming this is your download button
        // Similarly, get other buttons like 'set path'

        if (currentState === 'ANALYSIS') {
            analyzeBtn.disabled = true;
            downloadBtn.disabled = true;
            // Set other buttons as needed
        } else if (currentState === 'DOWNLOAD') {
            analyzeBtn.disabled = true;
            downloadBtn.disabled = true;
            // Set other buttons as needed
        } else {
            analyzeBtn.disabled = false;
            downloadBtn.disabled = false;
            // Set other buttons as needed
        }
    }
}

export default TableManager;