#!/usr/bin/env node

import assert from 'node:assert/strict'

const repoPattern = /^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/

function normalizeRepo(value) {
  const repo = value
    .trim()
    .replace(/^https:\/\/github\.com\//, '')
    .replace(/\/$/, '')
    .replace(/\.git$/, '')

  if (!repoPattern.test(repo)) {
    throw new Error(`Invalid repository: ${value}`)
  }

  return repo
}

function selfTest() {
  assert.equal(normalizeRepo('aidenybai/react-scan'), 'aidenybai/react-scan')
  assert.equal(normalizeRepo('https://github.com/vuejs/devtools.git'), 'vuejs/devtools')
  assert.equal(normalizeRepo('https://github.com/vuejs/devtools.git/'), 'vuejs/devtools')
  assert.throws(() => normalizeRepo('not-a-repository'))
  console.log('github-stars self-test passed')
}

async function fetchStars(repo, token) {
  const [owner, name] = repo.split('/')
  const headers = {
    Accept: 'application/vnd.github+json',
    'User-Agent': 'manage-frontend-debug-tools',
    'X-GitHub-Api-Version': '2022-11-28',
  }

  if (token) headers.Authorization = `Bearer ${token}`

  const response = await fetch(
    `https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(name)}`,
    { headers },
  )

  if (!response.ok) {
    throw new Error(`${repo}: GitHub API returned ${response.status}`)
  }

  const data = await response.json()
  return {
    repository: data.full_name,
    stars: data.stargazers_count,
    url: data.html_url,
  }
}

async function main(args) {
  if (args.includes('--self-test')) {
    selfTest()
    return
  }

  const json = args.includes('--json')
  const repos = args.filter((arg) => !arg.startsWith('--')).map(normalizeRepo)
  if (repos.length === 0) {
    throw new Error('Usage: github-stars.mjs [--json] owner/repository ...')
  }

  const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN
  const checkedAt = new Date().toISOString()
  const results = await Promise.all(repos.map((repo) => fetchStars(repo, token)))
  const output = { checked_at: checkedAt, repositories: results }

  if (json) {
    console.log(JSON.stringify(output, null, 2))
    return
  }

  for (const result of results) {
    console.log(`${result.repository}\t${result.stars}\t${result.url}\t${checkedAt}`)
  }
}

main(process.argv.slice(2)).catch((error) => {
  console.error(error.message)
  process.exitCode = 1
})
