export class VideoItem {
    constructor(videoData) {
        this.download_status = videoData.download_status || 'N/A';
        this.watch_url = videoData.watch_url || 'N/A';
        this.title = videoData.title || 'N/A';
        this.author = videoData.author || 'N/A';
        this.length = videoData.length != null ? videoData.length.toString() : 'N/A';
        this.description = videoData.description || 'N/A';
        this.publish_date = videoData.publish_date || 'N/A';
        this.views = videoData.views != null ? videoData.views.toString() : 'N/A';
        this.thumbnail_url = videoData.thumbnail_url || 'N/A';
        this.rating = videoData.rating || 'N/A';
        this.video_id = videoData.video_id || 'N/A';
        this.quality_str = videoData.quality_str || 'N/A';
        this.video_size_mb = videoData.video_size_mb != null ? videoData.video_size_mb.toString() : 'N/A';
    }

    toTableRow(index) {
        return `
            <td>${index + 1}</td>
            <td>${this.download_status}</td>
            <td>${this.watch_url}</td>
            <td>${this.title}</td>
            <td>${this.author}</td>
            <td>${this.length}</td>
            <td>${this.description}</td>
            <td>${this.publish_date}</td>
            <td>${this.views}</td>
            <td>${this.thumbnail_url}</td>
            <td>${this.rating}</td>
            <td>${this.video_id}</td>
            <td>${this.quality_str}</td>
            <td>${this.video_size_mb}</td>
        `;
    }
}
