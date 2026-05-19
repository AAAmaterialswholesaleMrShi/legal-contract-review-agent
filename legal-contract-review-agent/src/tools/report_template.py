"""Report template utility for generating standardized risk reports."""


REPORT_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Contract Risk Report</title>
    <style>
        body { font-family: sans-serif; margin: 40px; }
        h1 { color: #1a1a2e; }
    </style>
</head>
<body>
    <h1>Contract Risk Report</h1>
    {{ content }}
</body>
</html>
"""
