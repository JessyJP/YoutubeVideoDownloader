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
    }

    // toTableRow(index) {
    //     return `
    //         <td>${index + 1}</td>
    //         <td>${this.download_status}</td>
    //         <td>${this.watch_url}</td>
    //         <td>${this.title}</td>
    //         <td>${this.author}</td>
    //         <td>${this.length}</td>
    //         <td>${this.description}</td>
    //         <td>${this.publish_date}</td>
    //         <td>${this.views}</td>
    //         <td>${this.thumbnail_url}</td>
    //         <td>${this.rating}</td>
    //         <td>${this.video_id}</td>
    //         <td>${this.quality_str}</td>
    //         <td>${this.video_size_mb}</td>
    //     `;
    // }

    toTableRow(index) {
        return `
            <td>${index + 1}</td>
            <td>${this.download_status}</td>
            <td><a href="#" data-watch-url="${this.watch_url}">${this.watch_url}</a></td>
            <td><a href="#" data-title-url="${this.watch_url}">${this.title}</a></td>
            <td>${this.author}</td>
            <td>${this.length}</td>
            <td>--</td>
            <td>${this.publish_date}</td>
            <td>${this.views}</td>
            <td><img src="${this.thumbnail_url}" class="thumbnail-image"></td>
            <td>${this.rating}</td>
            <td>${this.video_id}</td>
            <td>${this.quality_str}</td>
            <td>${this.video_size_mb}</td>
        `;
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