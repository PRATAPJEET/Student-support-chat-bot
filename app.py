$path = "app.py"
$content = Get-Content $path -Raw

# The target match signature from your code structure
$target = 'theme_choice = st.sidebar.selectbox("Interface Theme", ["Light Mode 🌞", "Dark Mode 🌙"])'

$injection = @"

if "Light Mode" in theme_choice:
    st.markdown(\"\"\"
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
                background-color: #F1F5F9 !important;
            }
            [data-testid="stSidebar"] *, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p {
                color: #0F172A !important;
            }
            .stApp, [data-testid="stAppViewContainer"] {
                background-color: #FFFFFF !important;
                color: #0F172A !important;
            }
            h1, h2, h3, p, span, div.stMarkdownContainer {
                color: #0F172A !important;
            }
            [data-testid="stBaseButton-secondary"] {
                background-color: #E2E8F0 !important;
                color: #0F172A !important;
                border: 1px solid #CBD5E1 !important;
            }
            [data-testid="stBaseButton-secondary"] * {
                color: #0F172A !important;
            }
        </style>
    \"\"\", unsafe_allow_html=True)
else:
    st.markdown(\"\"\"
        <style>
            [data-testid="stSidebar"], [data-testid="stSidebarContent"] {
                background-color: #0F172A !important;
            }
            [data-testid="stSidebar"] *, [data-testid="stSidebar"] span, [data-testid="stSidebar"] p {
                color: #F8FAFC !important;
            }
            .stApp, [data-testid="stAppViewContainer"] {
                background-color: #0B0F19 !important;
                color: #F8FAFC !important;
            }
            h1, h2, h3, p, span, div.stMarkdownContainer {
                color: #F8FAFC !important;
            }
            [data-testid="stBaseButton-secondary"] {
                background-color: #1E293B !important;
                color: #F8FAFC !important;
                border: 1px solid #334155 !important;
            }
            [data-testid="stBaseButton-secondary"] * {
                color: #F8FAFC !important;
            }
        </style>
    \"\"\", unsafe_allow_html=True)
"@

if ($content -match [regex]::Escape($target)) {
    $newContent = $content -replace [regex]::Escape($target), ($target + "`n" + $injection)
    Set-Content -Path $path -Value $newContent -Encoding utf8
    Write-Host "✅ app.py successfully updated via automation!" -ForegroundColor Green
} else {
    Write-Host "❌ Target dropdown string not found. Please review the selectbox variable name in app.py." -ForegroundColor Red
}