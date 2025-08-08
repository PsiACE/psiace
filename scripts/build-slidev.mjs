#!/usr/bin/env node
import { execSync } from 'node:child_process'
import fs from 'node:fs'
import path from 'node:path'

const projectRoot = path.resolve('.')
const slidesDir = path.join(projectRoot, 'src', 'content', 'slide')
const outputDir = path.join(projectRoot, 'public', 'slides-embed')
const tmpDir = path.join(projectRoot, '.slidev-tmp')

function getBasePathFromSiteConfig() {
  try {
    const cfg = fs.readFileSync(path.join(projectRoot, 'src', 'site.config.ts'), 'utf8')
    const m = cfg.match(/url:\s*"([^"]+)"/)
    if (m && m[1]) {
      const u = new URL(m[1])
      let p = u.pathname || '/'
      if (p !== '/' && p.endsWith('/')) p = p.slice(0, -1)
      return p === '/' ? '' : p
    }
  } catch {}
  return ''
}
const basePath = getBasePathFromSiteConfig()

if (!fs.existsSync(slidesDir)) {
  console.log(`[build-slidev] No slides directory found at ${slidesDir}, skipping.`)
  process.exit(0)
}

fs.mkdirSync(outputDir, { recursive: true })
fs.mkdirSync(tmpDir, { recursive: true })

function* walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) {
      yield* walk(full)
    } else if (entry.isFile() && /\.(md|mdx)$/.test(entry.name)) {
      yield full
    }
  }
}

const entries = Array.from(walk(slidesDir))

for (const inputPath of entries) {
  const rel = path.relative(slidesDir, inputPath)
  const slug = rel.replace(/\\/g, '/').replace(/\.(md|mdx)$/i, '')
  const outDir = path.join(outputDir, slug)
  fs.mkdirSync(outDir, { recursive: true })


  const base = `${basePath}/slides-embed/${slug}/`
  const cmd = `pnpm exec slidev build "${inputPath}" --out "${outDir}" --base "${base}"`
  console.log(`[build-slidev] Building ${rel} -> ${outDir}`)
  try {
    execSync(cmd, { stdio: 'inherit' })
    // Ensure favicon/icon exists to avoid 404s in iframe (handle nested bad hrefs)
    const siteIconPrimary = path.join(projectRoot, 'public', 'icon.svg')
    const siteIconAlt = path.join(projectRoot, 'public', 'favicon.svg')
    const sourceIcon = fs.existsSync(siteIconPrimary)
      ? siteIconPrimary
      : (fs.existsSync(siteIconAlt) ? siteIconAlt : null)

    const copyIconTo = (targetDir) => {
      const iconPath = path.join(targetDir, 'icon.svg')
      const faviconPath = path.join(targetDir, 'favicon.svg')
      if (sourceIcon) {
        if (!fs.existsSync(iconPath)) fs.copyFileSync(sourceIcon, iconPath)
        if (!fs.existsSync(faviconPath)) fs.copyFileSync(sourceIcon, faviconPath)
      } else {
        if (!fs.existsSync(iconPath)) fs.writeFileSync(iconPath, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="8" fill="#111"/></svg>', 'utf8')
        if (!fs.existsSync(faviconPath)) fs.writeFileSync(faviconPath, '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><circle cx="8" cy="8" r="8" fill="#111"/></svg>', 'utf8')
      }
    }
    try {
      // depth 0: outDir itself
      copyIconTo(outDir)
      // depths 1..3: handle repeated "slides-embed/<slug>" segments in hrefs
      let base = outDir
      for (let i = 1; i <= 3; i++) {
        base = path.join(base, 'slides-embed', slug)
        fs.mkdirSync(base, { recursive: true })
        copyIconTo(base)
      }
    } catch {}
  } catch (err) {
    console.error(`[build-slidev] Failed to build ${rel}:`, err?.message || err)
    process.exitCode = 1
  }
}
