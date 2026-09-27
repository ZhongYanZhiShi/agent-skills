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

async function selfTest() {
  assert.equal(normalizeRepo('aidenybai/react-scan'), 'aidenybai/react-scan')
  assert.equal(normalizeRepo('https://github.com/vuejs/devtools.git'), 'vuejs/devtools')
  assert.equal(normalizeRepo('https://github.com/vuejs/devtools.git/'), 'vuejs/devtools')
  assert.throws(() => normalizeRepo('not-a-repository'))
  const output = await queryStars(['good/repo', 'missing/repo', 'offline/repo'], undefined, async url => {
    if (url.endsWith('/offline/repo')) throw new Error('Network unavailable')
    return url.endsWith('/good/repo')
      ? { ok: true, json: async () => ({ full_name: 'good/repo', stargazers_count: 123, html_url: 'https://github.com/good/repo' }) }
      : { ok: false, status: 404 }
  })
  assert.deepEqual(output.repositories, [{ repository: 'good/repo', stars: 123, url: 'https://github.com/good/repo' }])
  assert.deepEqual(output.errors, [
    { repository: 'missing/repo', error: 'GitHub API returned 404' },
    { repository: 'offline/repo', error: 'Network unavailable' },
  ])
  console.log('github-stars self-test passed')
}

async function fetchStars(repo, token, fetchImpl) {
  const [owner, name] = repo.split('/')
  const headers = {
    Accept: 'application/vnd.github+json',
    'User-Agent': 'manage-frontend-debug-tools',
    'X-GitHub-Api-Version': '2022-11-28',
  }

  if (token) headers.Authorization = `Bearer ${token}`

  const response = await fetchImpl(
    `https://api.github.com/repos/${encodeURIComponent(owner)}/${encodeURIComponent(name)}`,
    { headers, signal: AbortSignal.timeout(10_000) },
  )

  if (!response.ok) {
    throw new Error(`GitHub API returned ${response.status}`)
  }

  const data = await response.json()
  return {
    repository: data.full_name,
    stars: data.stargazers_count,
    url: data.html_url,
  }
}

async function queryStars(repos, token, fetchImpl = fetch) {
  const settled = await Promise.allSettled(repos.map(repo => fetchStars(repo, token, fetchImpl)))
  const repositories = []
  const errors = []
  settled.forEach((result, index) => {
    if (result.status === 'fulfilled') repositories.push(result.value)
    else errors.push({ repository: repos[index], error: result.reason.message })
  })
  return { repositories, errors }
}

async function main(args) {
  if (args.includes('--self-test')) {
    await selfTest()
    return
  }

  const json = args.includes('--json')
  const repos = args.filter((arg) => !arg.startsWith('--')).map(normalizeRepo)
  if (repos.length === 0) {
    throw new Error('Usage: github-stars.mjs [--json] owner/repository ...')
  }

  const token = process.env.GITHUB_TOKEN || process.env.GH_TOKEN
  const checkedAt = new Date().toISOString()
  const output = { checked_at: checkedAt, ...await queryStars(repos, token) }
  if (output.errors.length) process.exitCode = 1

  if (json) {
    console.log(JSON.stringify(output, null, 2))
    return
  }

  for (const result of output.repositories) {
    console.log(`${result.repository}\t${result.stars}\t${result.url}\t${checkedAt}`)
  }
  for (const result of output.errors) console.error(`${result.repository}: ${result.error}`)
}

main(process.argv.slice(2)).catch((error) => {
  console.error(error.message)
  process.exitCode = 1
})
