document.getElementById('generateForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const keyword = document.getElementById('keyword').value;
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    
    // Show loading spinner
    loading.style.display = 'block';
    result.style.display = 'none';
    
    try {
        const response = await fetch(`/generate?keyword=${encodeURIComponent(keyword)}`);
        const data = await response.json();
        
        if (response.ok) {
            // Update the UI with the generated content
            document.getElementById('blogTitle').textContent = data.blog.title || '';
            document.getElementById('metaDescription').textContent = data.blog.meta_description || '';
            document.getElementById('searchVolume').textContent = (data.seo_metrics.search_volume || 0).toLocaleString();
            document.getElementById('keywordDifficulty').textContent = data.seo_metrics.keyword_difficulty || 0;
            document.getElementById('avgCpc').textContent = (data.seo_metrics.avg_cpc || 0).toFixed(2);
            
            // Process the content to replace affiliate link placeholders
            let processedContent = data.blog.content || '';
            
            // Replace affiliate link placeholders with actual product links
            const affiliateLinks = {
                '{{AFF_LINK_1}}': 'https://amazon.com/recommended-product-1',
                '{{AFF_LINK_2}}': 'https://amazon.com/recommended-product-2',
                '{{AFF_LINK_3}}': 'https://amazon.com/recommended-product-3'
            };

            // Replace affiliate links with HTML
            Object.entries(affiliateLinks).forEach(([placeholder, link]) => {
                const safePlaceholder = placeholder.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
                const regex = new RegExp(safePlaceholder, 'g');
                processedContent = processedContent.replace(
                    regex,
                    `<a href="${link}" target="_blank" rel="nofollow" class="affiliate-link">View on Amazon</a>`
                );
            });

            try {
                // Set up basic marked options
                marked.setOptions({
                    breaks: true,
                    gfm: true,
                    headerIds: false,
                    mangle: false,
                    sanitize: false
                });

                // Convert markdown to HTML
                const htmlContent = marked.parse(processedContent);
                
                // Create a safe container for the content
                const contentContainer = document.createElement('div');
                contentContainer.className = 'blog-content';
                contentContainer.innerHTML = htmlContent;

                // Replace the content
                const blogContent = document.getElementById('blogContent');
                blogContent.innerHTML = '';
                blogContent.appendChild(contentContainer);
            } catch (markdownError) {
                console.error('Markdown parsing error:', markdownError);
                // Fallback to basic HTML rendering
                const contentContainer = document.createElement('div');
                contentContainer.className = 'blog-content';
                contentContainer.innerHTML = processedContent
                    .split('\n')
                    .map(line => `<p>${line}</p>`)
                    .join('');
                
                const blogContent = document.getElementById('blogContent');
                blogContent.innerHTML = '';
                blogContent.appendChild(contentContainer);
            }
            
            // Show the result
            result.style.display = 'block';
            
            // Scroll to result
            result.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            throw new Error(data.error || 'Failed to generate content');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error: ' + (error.message || 'Failed to generate content'));
    } finally {
        // Hide loading spinner
        loading.style.display = 'none';
    }
}); 