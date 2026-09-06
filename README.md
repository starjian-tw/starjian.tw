# starjian.tw

星鑑科技工作室的部落格。Hugo ＋ PaperMod，GitHub Pages 代管，GitHub Actions 自動建站。

## 發文流程

1. 在 `content/posts/` 新增 Markdown，檔名 `YYYY-MM-DD-slug.md`，front matter 照既有文章。
2. `draft: true` 的文章不會出現在正式站；核對完改成 `false`。
3. `git push` 到 `main`，Actions 會自動建站並部署，約一到兩分鐘。

## 第一次上線要做的事（只做一次）

1. GitHub 建公開 repo，推上這個資料夾。
2. Repo → Settings → Pages → Build and deployment → Source 選 **GitHub Actions**。
3. Settings → Pages → Custom domain 填 `starjian.tw`，勾 **Enforce HTTPS**（DNS 生效後才勾得起來）。
4. Gandi DNS：

| 類型 | 名稱 | 值 |
|------|------|-----|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | `<GitHub 帳號>.github.io.` |

刪掉 Gandi 預設的 `@` A（217.70.184.38）與 `www` CNAME（webredir）。

## 本機預覽（可選）

裝 Hugo extended 後：

```
git clone --depth 1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod
hugo server -D
```

`themes/` 在 `.gitignore` 裡，CI 會自己抓，不用提交。
