#!/usr/bin/env python3
"""
PDF Generator for MedHealth System Documentation
Converts markdown documentation to PDF
"""

try:
    from markdown import markdown
    from weasyprint import HTML, CSS
    import os
    
    def generate_pdf():
        # Read markdown file
        with open('MEDHEALTH_SYSTEM_DOCUMENTATION.md', 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html_content = markdown(md_content, extensions=['extra', 'codehilite'])
        
        # Add CSS styling
        html_with_style = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 40px;
                    color: #333;
                }}
                h1 {{
                    color: #2c3e50;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    border-bottom: 2px solid #95a5a6;
                    padding-bottom: 5px;
                    margin-top: 30px;
                }}
                h3 {{
                    color: #555;
                    margin-top: 20px;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin: 20px 0;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                code {{
                    background-color: #f4f4f4;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                }}
                pre {{
                    background-color: #f4f4f4;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                }}
                blockquote {{
                    border-left: 4px solid #3498db;
                    margin: 20px 0;
                    padding-left: 20px;
                    color: #555;
                }}
                ul, ol {{
                    margin: 10px 0;
                    padding-left: 30px;
                }}
                .page-break {{
                    page-break-after: always;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Generate PDF
        HTML(string=html_with_style).write_pdf('MEDHEALTH_SYSTEM_DOCUMENTATION.pdf')
        print("✓ PDF generated successfully: MEDHEALTH_SYSTEM_DOCUMENTATION.pdf")
        
    if __name__ == "__main__":
        generate_pdf()
        
except ImportError:
    print("PDF generation libraries not installed.")
    print("To generate PDF, install: pip install markdown weasyprint")
    print("\nAlternatively, you can:")
    print("1. Open MEDHEALTH_SYSTEM_DOCUMENTATION.md in a markdown viewer")
    print("2. Use 'Print to PDF' from your browser or markdown editor")
    print("3. Use online markdown to PDF converters")

