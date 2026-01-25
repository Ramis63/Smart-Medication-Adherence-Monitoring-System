#!/usr/bin/env python3
"""
HTML/PDF Generator for MedHealth System Documentation
Creates an HTML file that can be easily printed to PDF from browser
"""

from markdown import markdown
import os

def generate_html():
    # Read markdown file
    with open('MEDHEALTH_SYSTEM_DOCUMENTATION.md', 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    html_content = markdown(md_content, extensions=['extra', 'codehilite', 'tables'])
    
    # Add comprehensive CSS styling for PDF printing
    html_with_style = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Smart Medication Adherence and Health Monitoring System - Complete Documentation</title>
        <style>
            @media print {{
                @page {{
                    size: A4;
                    margin: 2cm;
                }}
                body {{
                    font-size: 11pt;
                }}
                h1 {{
                    page-break-after: avoid;
                }}
                h2 {{
                    page-break-after: avoid;
                }}
                table {{
                    page-break-inside: avoid;
                }}
            }}
            
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                margin: 40px;
                color: #333;
                max-width: 900px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            h1 {{
                color: #2c3e50;
                border-bottom: 4px solid #3498db;
                padding-bottom: 15px;
                margin-top: 0;
                font-size: 28px;
            }}
            
            h2 {{
                color: #34495e;
                border-bottom: 2px solid #95a5a6;
                padding-bottom: 8px;
                margin-top: 35px;
                font-size: 22px;
                page-break-after: avoid;
            }}
            
            h3 {{
                color: #555;
                margin-top: 25px;
                font-size: 18px;
            }}
            
            h4 {{
                color: #666;
                margin-top: 20px;
                font-size: 16px;
            }}
            
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
                font-size: 14px;
                page-break-inside: avoid;
            }}
            
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            
            th {{
                background-color: #3498db;
                color: white;
                font-weight: bold;
            }}
            
            tr:nth-child(even) {{
                background-color: #f8f9fa;
            }}
            
            code {{
                background-color: #f4f4f4;
                padding: 3px 8px;
                border-radius: 3px;
                font-family: 'Courier New', 'Consolas', monospace;
                font-size: 13px;
                border: 1px solid #e0e0e0;
            }}
            
            pre {{
                background-color: #f4f4f4;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
                border: 1px solid #e0e0e0;
                font-size: 12px;
            }}
            
            pre code {{
                background-color: transparent;
                padding: 0;
                border: none;
            }}
            
            blockquote {{
                border-left: 4px solid #3498db;
                margin: 20px 0;
                padding-left: 20px;
                color: #555;
                font-style: italic;
                background-color: #f8f9fa;
                padding: 15px 20px;
            }}
            
            ul, ol {{
                margin: 15px 0;
                padding-left: 35px;
            }}
            
            li {{
                margin: 8px 0;
            }}
            
            p {{
                margin: 12px 0;
            }}
            
            strong {{
                color: #2c3e50;
            }}
            
            .page-break {{
                page-break-after: always;
            }}
            
            hr {{
                border: none;
                border-top: 2px solid #ecf0f1;
                margin: 30px 0;
            }}
            
            .warning {{
                background-color: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                margin: 20px 0;
            }}
            
            .info {{
                background-color: #d1ecf1;
                border-left: 4px solid #17a2b8;
                padding: 15px;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        {html_content}
        
        <div style="margin-top: 50px; padding-top: 20px; border-top: 2px solid #ecf0f1; text-align: center; color: #7f8c8d; font-size: 12px;">
            <p>Smart Medication Adherence and Health Monitoring System - Complete Documentation</p>
            <p>Version 1.0 | TH Deggendorf - Health Informatics</p>
        </div>
    </body>
    </html>
    """
    
    # Write HTML file
    with open('MEDHEALTH_SYSTEM_DOCUMENTATION.html', 'w', encoding='utf-8') as f:
        f.write(html_with_style)
    
    print("HTML file generated successfully: MEDHEALTH_SYSTEM_DOCUMENTATION.html")
    print("\nTo create PDF:")
    print("1. Open MEDHEALTH_SYSTEM_DOCUMENTATION.html in your web browser")
    print("2. Press Ctrl+P (Print)")
    print("3. Select 'Save as PDF' or 'Microsoft Print to PDF' as printer")
    print("4. Click 'Save' and choose location")
    print("\nThe HTML file is ready for PDF conversion!")

if __name__ == "__main__":
    generate_html()

