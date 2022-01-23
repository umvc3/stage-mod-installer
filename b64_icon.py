from base64 import b64encode

# run this program and paste result into this string
#       v
icon = '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'

# python3 b64_icon.py | clip

if __name__ == '__main__':
    with open('icon\\icon.png', 'rb') as f:
        print(b64encode(f.read()).decode('utf-8'))