import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace all occurrences of 'md:' inside class attributes with '@md:'
content = re.sub(r'([\"\'\s])md:', r'\1@md:', content)

# Wrap the body contents in an @container div
body_start_match = re.search(r'<body[^>]*>', content)
if body_start_match:
    body_start_idx = body_start_match.end()
    body_end_idx = content.rfind('</body>')
    
    wrapper_start = '\n<div id=\"app-container\" class=\"@container w-full h-full relative transition-all duration-500 ease-in-out\">\n'
    wrapper_end = '\n</div>\n'
    
    new_content = content[:body_start_idx] + wrapper_start + content[body_start_idx:body_end_idx] + wrapper_end + content[body_end_idx:]
    
    # Also add the toggle button inside the body but outside the app-container
    toggle_btn_html = '''
    <button id="mode-toggle" onclick="toggleMode()" class="fixed top-4 right-4 z-[9999] bg-surface-container-high border border-outline-variant text-on-surface px-4 py-2 rounded-full shadow-xl font-mono text-label-md hover:bg-surface-variant transition-colors flex items-center gap-2">
        <span class="material-symbols-outlined text-[18px]" id="mode-icon">phone_iphone</span>
        <span id="mode-text">Mobile Mode</span>
    </button>
    
    <script>
        let isMobileMode = false;
        function toggleMode() {
            isMobileMode = !isMobileMode;
            const container = document.getElementById('app-container');
            const body = document.body;
            const text = document.getElementById('mode-text');
            const icon = document.getElementById('mode-icon');
            
            if (isMobileMode) {
                // Switch to Mobile Mode
                body.classList.add('flex', 'items-center', 'justify-center', 'bg-black');
                container.className = '@container w-[390px] h-[844px] overflow-hidden rounded-[40px] border-[12px] border-surface shadow-2xl relative transition-all duration-500 ease-in-out flex-shrink-0 mt-8';
                
                text.innerText = 'Desktop Mode';
                icon.innerText = 'desktop_windows';
            } else {
                // Switch to Desktop Mode
                body.classList.remove('flex', 'items-center', 'justify-center', 'bg-black');
                container.className = '@container w-full h-full relative transition-all duration-500 ease-in-out';
                
                text.innerText = 'Mobile Mode';
                icon.innerText = 'phone_iphone';
            }
        }
    </script>
    '''
    
    body_end_idx = new_content.rfind('</body>')
    new_content = new_content[:body_end_idx] + toggle_btn_html + new_content[body_end_idx:]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print('Updated index.html successfully')
else:
    print('Could not find body tag')
