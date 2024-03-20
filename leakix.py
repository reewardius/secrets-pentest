import requests
import re
import argparse
import time
from urllib.parse import quote

def search_leakix(query, output_file=None):
    url = 'https://leakix.net/search'
    params = {'scope': 'leak', 'q': f'"{query}"'}  # Add quotes around the query
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    }

    response = requests.get(url, params=params, headers=headers)

    if response.ok:
        match = re.search(r'<em>Found (\d+) results for <pre style="white-space: pre-wrap; ">&#34;{}&#34;</pre></em>'.format(re.escape(query)), response.text)
        if match:
            num_results = match.group(1)
            output = f"Found {num_results} results for {query}"
            if output_file:
                with open(output_file, 'a') as f:
                    f.write(output + '\n')
            else:
                print(output)
    else:
        print(f"Failed to retrieve data from Leakix for {query}")

    time.sleep(2)

def main():
    parser = argparse.ArgumentParser(description='Search Leakix')
    parser.add_argument('-d', '--domain', type=str, help='Single domain to search')
    parser.add_argument('-l', '--list', type=str, help='File containing list of domains')
    parser.add_argument('-o', '--output', type=str, help='Output file name')
    args = parser.parse_args()

    if args.domain:
        search_leakix(args.domain, args.output)
    elif args.list:
        with open(args.list, 'r') as file:
            for line in file:
                query = line.strip()
                search_leakix(query, args.output)
    else:
        print("Please provide a domain using the -d flag or a file containing domains using the -l flag")

if __name__ == "__main__":
    main()
