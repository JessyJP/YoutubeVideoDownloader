export class VideoItem {
    constructor(videoData) {
        this.download_status = videoData.download_status;
        this.watch_url = videoData.watch_url;
        this.title = videoData.title;
        this.author = videoData.author;
        this.length = videoData.length != null ? videoData.length.toString() : 'N/A';
        this.description = videoData.description;
        this.publish_date = videoData.publish_date;
        this.views = videoData.views != null ? videoData.views.toString() : 'N/A';
        this.thumbnail_url = videoData.thumbnail_url;
        this.rating = videoData.rating;
        this.video_id = videoData.video_id;
        this.quality_str = videoData.quality_str;
        this.video_size_mb = videoData.video_size_mb != null ? videoData.video_size_mb.toString() : 'N/A';
        // Extra argument
        this.itemIsSelected = false;
        // Bind the handleRowClick method to the class instance
        this.handleRowClick = this.handleRowClick.bind(this);
    }

    toTableRowDefault(index) {
        return `
            <td>${index + 1}</td>
            <td>${this.download_status}</td>
            <td><a href="#" data-watch-url="${this.watch_url}">${this.watch_url}</a></td>
            <td><a href="#" data-title-url="${this.watch_url}">${this.title}</a></td>
            <td>${this.author}</td>
            <td>${this.length}</td>
            <td>${this.publish_date}</td>
            <td>${this.views}</td>
            <td><img src="${this.thumbnail_url}" class="thumbnail-image"></td>
            <td>${this.rating}</td>
            <td>${this.video_id}</td>
            <td>${this.quality_str}</td>
            <td>${this.video_size_mb}</td>
            <td>${this.description}</td>
        `;
    }


    toTableRow(index, columnState, itemIsSelected = undefined) {
        let rowHTML = '';
        // Check if itemIsSelected is a boolean before assigning
        if (typeof itemIsSelected === 'boolean') {
            this.itemIsSelected = itemIsSelected;
        }

        // Sort the columnState by order before building the row
        columnState.sort((a, b) => a.order - b.order);

        columnState.forEach(column => {
            if (column.isVisible) {
                switch (column.label) {
                    case 'Index':
                        rowHTML += `<td>${index + 1}</td>`;
                        break;
                    case 'Download Status':
                        rowHTML += `<td>${this.download_status}</td>`;
                        break;
                    case 'Watch URL':
                        rowHTML += `<td><a href="#" data-watch-url="${this.watch_url}">${this.watch_url}</a></td>`;
                        break;
                    case 'Title':
                        rowHTML += `<td><a href="#" data-title-url="${this.watch_url}">${this.title}</a></td>`;
                        break;
                    case 'Author':
                        rowHTML += `<td>${this.author}</td>`;
                        break;
                    case 'Length':
                        rowHTML += `<td>${this.length}</td>`;
                        break;
                    case 'Description':
                        rowHTML += `<td>${this.description}</td>`;
                        break;
                    case 'Publish Date':
                        rowHTML += `<td>${this.publish_date}</td>`;
                        break;
                    case 'Views':
                        rowHTML += `<td>${this.views}</td>`;
                        break;
                    case 'Thumbnail URL':
                        rowHTML += `<td><img src="${this.thumbnail_url}" class="thumbnail-image"></td>`;
                        break;
                    case 'Rating':
                        rowHTML += `<td>${this.rating}</td>`;
                        break;
                    case 'Video ID':
                        rowHTML += `<td>${this.video_id}</td>`;
                        break;
                    case 'Quality':
                        rowHTML += `<td>${this.quality_str}</td>`;
                        break;
                    case 'File Size (MB)':
                        rowHTML += `<td>${this.video_size_mb}</td>`;
                        break;
                    // Add cases for any other columns you might have
                }
            }
        });

        // Create the table row element
        const row = document.createElement('tr');
        row.innerHTML = rowHTML;
        row.dataset.videoId = this.video_id;
        row.className = this.itemIsSelected ? 'item-selected' : '';

        // Attach the handleRowClick method as an event listener
        row.addEventListener('click', this.handleRowClick); // Corrected here

        return row; // Return the row element directly
    }

    toGridCard(index, columnState) {
        let thumbnailHTML = '';
        let titleHTML = '';
        let authorHTML = '';
        let lengthHTML = '';
        let descriptionHTML = '';
        let viewsHTML = '';
        let publishDateHTML = '';
        let watchLinkHTML = '';
        let ratingHTML = '';
    
        // Sort the columnState by order before building the card
        columnState.sort((a, b) => a.order - b.order);
    
        columnState.forEach(column => {
            if (column.isVisible) {
                switch (column.label) {
                    case 'Thumbnail URL':
                        thumbnailHTML = `<img src="${this.thumbnail_url}" class="video-thumbnail" alt="Thumbnail">`;
                        break;
                    case 'Title':
                        titleHTML = `<h3 class="video-title">${this.title}</h3>`;
                        break;
                    case 'Author':
                        authorHTML = `<p class="video-author">${this.author}</p>`;
                        break;
                    case 'Length':
                        lengthHTML = `<p class="video-length">${this.length}</p>`;
                        break;
                    case 'Description':
                        descriptionHTML = `<p class="video-description">${this.description}</p>`;
                        break;
                    case 'Views':
                        viewsHTML = `<span class="video-views">${this.views} views</span>`;
                        break;
                    case 'Publish Date':
                        publishDateHTML = `<span class="video-publish-date">${this.publish_date}</span>`;
                        break;
                    case 'Watch URL':
                        watchLinkHTML = `<a href="#" class="video-watch-link" data-watch-url="${this.watch_url}">Watch</a>`;
                        break;
                    case 'Rating':
                        ratingHTML = `<span class="video-rating">${this.rating}</span>`;
                        break;
                    // Add cases for any other columns you might have
                }
            }
        });
            
        // Create the grid card element
        const card = document.createElement('div');
        card.classList.add('video-card');
        card.dataset.videoId = this.video_id;
        card.innerHTML = `
            ${thumbnailHTML}
            <div class="video-info">
                ${titleHTML}
                ${authorHTML}
                ${lengthHTML}
                ${descriptionHTML}
                <div class="video-meta">
                    ${viewsHTML}
                    ${publishDateHTML}
                </div>
                <div class="video-actions">
                    ${watchLinkHTML}
                    ${ratingHTML}
                </div>
            </div>
        `;
        
        // Attach the handleRowClick method as an event listener
        card.addEventListener('click', this.handleRowClick);
    
        return card; // Return the card element directly
    }
    
    

    handleRowClick(event) {
        // Ignore clicks on links or other interactive elements
        if (event.target.tagName === 'A' || event.target.tagName === 'BUTTON' || event.target.tagName === 'INPUT') {
            return;
        }

        // Toggle the selection state
        this.itemIsSelected = !this.itemIsSelected;

        // Update the UI for this row
        const row = event.currentTarget;
        row.classList.toggle('item-selected', this.itemIsSelected);
    }
}


export function assignUrlClickListener(link) {
    link.addEventListener('click', (event) => {
        event.preventDefault();
        const url = link.getAttribute('data-watch-url');
        console.log('Link clicked:', url);
        window.open(url, '_blank');
    });
}


export function assignTitleClickListener(link) {
    link.addEventListener('click', (event) => {
        event.preventDefault();
        const url = link.getAttribute('data-title-url');
        console.log('Title link clicked:', url);
        // Handle the title URL click event here
        // For example, you might want to open the URL in a new tab
        window.open(url, '_blank');
    });
}