import os
import requests

# GitHub GraphQL API endpoint
graphql_url = 'https://api.github.com/graphql'

# Get necessary information from the environment
username = os.environ['GITHUB_REPOSITORY'].split("/")[0]
# repo is like USERNAME/REPO_NAME
repo = os.environ['GITHUB_REPOSITORY'].split("/")[1]

# GraphQL query to get the title of the latest discussion
graphql_query = """
query {
  repository(owner: "%(username)s", name: "%(repo)s") {
    discussions(first: 1, orderBy: { field: CREATED_AT, direction: DESC }) {
      nodes {
        title
        number
      }
    }
  }
}
""" % {"username": username, "repo": repo}

# Fetch discussion details
headers = {
    "Authorization": f"Bearer {os.environ['GH_TOKEN']}",
    'Content-Type': 'application/json',
}

# Make the GraphQL request
response = requests.post(graphql_url, headers=headers, json={'query': graphql_query})
discussion_data = response.json()

# Check for a successful response
if response.status_code == 200:
    data = response.json()
    print(data)
    discussion_title = data['data']['repository']['discussions']['nodes'][0]['title']
    discussion_number = data['data']['repository']['discussions']['nodes'][0]['number']
    discussion_url = f"https://github.com/{username}/{repo}/discussions/{discussion_number}"
    # Update README.md
    readme_path = "README.md"
    with open(readme_path, "a") as readme_file:
        readme_file.write(f"\n- [{discussion_title}]({discussion_url})\n")
else:
    print(f"GraphQL request failed with status code {response.status_code}: {response.text}")
    exit(-1)
