+++
title = "Trying Jekyll with GitHub Pages"
description = "A quick start for Jekyll and GitHub Pages, including themes and customization."
date = 2018-07-14
slug = "try-jekyll-with-github"

[taxonomies]
tags = ["Jekyll", "GitHub Pages", "Static Site Generator"]

[extra]
lang = "en"
+++

*This article helps you get started quickly. To avoid spending too much time on introductions, please check the official websites and documentation for the parts you are interested in.*

[Jekyll](https://jekyllrb.com) is an excellent static site generator, and [GitHub Pages](https://pages.github.com) is a static page hosting service provided by **GitHub**. With them, we can easily build websites for projects or organizations, and we can also publish our own blogs and resumes.

One of the biggest advantages of using Jekyll and GitHub Pages together is that you can focus only on content. Many excellent designers and developers have made a large number of beautiful and practical themes for Jekyll, while GitHub saves us the cost of buying servers. The only limitation may be that we need third-party services for features such as comments and online forms.

This article introduces the following topics:

- Deploying a local Jekyll/GitHub Pages environment
- Enabling the GitHub Pages user page service
- Using excellent Jekyll themes
- The structure of a Jekyll theme
- Some third-party services and personalized configuration
- Publishing your page :)

All right, let us begin. Have fun.

## Deploying a Local Jekyll/GitHub Pages Environment

First, we need a computer connected to the internet. If you do not have one, do not worry. I may add a section later about how to complete this work with a phone.

You need to install the Ruby environment first. Here is the command-line installation method for Fedora:

```shell
sudo dnf install ruby ruby-devel
```

If you use Ubuntu, replace the command with:

```shell
sudo apt-get install ruby ruby-dev
```

As for `[Y/N]`, of course we choose Y :)

If you use Windows or another operating system, please refer to the [Ruby website](https://www.ruby-lang.org), where you can easily find the installation method.

Next, create a local environment using the dependency approach recommended by GitHub Pages. Install Bundler first, then use the `github-pages` gem in the project to align with the GitHub Pages environment:

```shell
gem install bundler
mkdir myblog
cd myblog
bundle init
```

Add this to `Gemfile`:

```ruby
gem "github-pages", group: :jekyll_plugins
```

Then run:

```shell
bundle install
bundle exec jekyll new . --force
bundle exec jekyll serve
```

The reason for not directly using `gem install bundler jekyll` is simply that we want to build an environment exactly consistent with GitHub Pages.

Enter the address it provides in your browser, perhaps `http://localhost:4000` or `http://127.0.0.1:4000/`, and you can see the official template.

If you like it, you can start working from there directly. Open the folder, create files under `_posts` in the format `yyyy-mm-dd-title.md` according to the example, edit the content, and then you can see the changes on the page. I will introduce more about this later.

## Enabling GitHub Pages User Pages

If you do not have a [GitHub](https://github.com) account yet, I strongly recommend registering one, because it is one of the most active social coding communities in the world. Visit the homepage and you can find the entry point.

I strongly recommend referring to GitHub's official documentation. It describes almost everything you may want to know in detail. Of course, you need some ability to read English documentation, or at least be able to use translation.

Now that you have a GitHub account, I usually recommend creating a repository named `yourusername.github.io`. Please allow it to initialize the repository with a README, especially when you only want to experiment and do not have content ready. This gives you a subdomain kindly provided by GitHub. All qualified content on the main branch, then called `master`, will be rebuilt and published. Usually, you can visit `https://yourusername.github.io` in your browser and see the converted content of `README.md`.

If it does not display correctly, or if you want to enable GitHub Pages in another repository, open the repository `Settings` and follow the instructions. If the page looks bare, you can choose an official theme through `Choose a theme`, but this is not necessary because we will introduce excellent Jekyll themes and further customization next.

## Using Excellent Jekyll Themes

Reinventing the wheel is interesting, but it often takes a lot of time, and a good idea may need a lot of debugging before it works properly. If you are not satisfied with Jekyll's default themes, I suggest trying some excellent Jekyll themes. They often implement:

- Responsive layout
- Good file structure
- Tag clouds and post categories
- Optimized SEO settings
- Third-party comment and analytics plugin support

Starting from an excellent Jekyll theme lets you focus more on the article itself rather than a large amount of CSS code :)

I especially recommend three themes:

- **[Huxblog-Boilerplate](https://github.com/Huxpro/huxblog-boilerplate)**, by [@Huxpro](https://github.com/Huxpro/), Apache License v2.0
- **[Jekyll NexT](https://github.com/Simpleyyt/jekyll-theme-next)**, by [@Simpleyyt](https://github.com/Simpleyyt/), Unknown
- **[Leonids](https://github.com/renyuanz/leonids)**, by [@renyuanz](https://github.com/renyuanz/), MIT License

Click the theme names to visit their repositories, then choose and download the one you like.

Trust me, we can completely avoid Git and its command-line tools. If you do not want to skip those, you may need to read another article. I do not plan to introduce them for now.

If you want to find more themes, I strongly recommend checking [Jekyll Themes](http://jekyllthemes.org) and choosing one you like.

## The Structure of a Jekyll Theme

I noticed that I had not explained how to use these Jekyll themes. It is actually very simple: `cd your-jekyll-theme`, `bundler install`, and `jekyll serve`. You can also get a local preview version in your browser. Even if the command you use does not include `--watch`, content generation will still be live.

I know you have had enough of empty themes, meaningless demo content, and my rambling, but please bear with me a little longer. Here we will talk about the structure of a Jekyll theme and some simple ways to organize content, which will help you modify and configure the theme next.

Open the folder of the theme you selected with a file manager or your favorite text editor, and see what is inside.

Usually, a Jekyll theme has a structure like this:

```text
.
├── _config.yml
├── _drafts
|   ├── begin-with-the-crazy-ideas.md
|   └── sample-and-test.markdown
├── _includes
|   ├── footer.html
|   └── header.html
├── _layouts
|   ├── default.html
|   └── post.html
├── _posts
|   ├── 2015-10-29-how-to-begin.textile
|   └── 2013-04-26-hello-world.md
├── _data
|   └── members.yml
├── _site
└── index.html
```

- `_config.yml`

  Stores configuration data. Many configuration options can be set directly from the command line, but if you write them here, you do not have to remember those commands.

- `_drafts`

  Drafts are unpublished posts. These files do not have `title.MARKUP` data in the filename.

- `_includes`

  You can load these included parts into your layouts or posts for reuse. Use `{% raw %}{% include file.ext %}{% endraw %}` to include `_includes/file.ext`.

- `_layouts`

  Layouts are templates wrapped around posts. Layouts can be selected in the YAML front matter for different posts. The tag `{% raw %}{{ content }}{% endraw %}` inserts content into the page.

- `_posts`

  This is where your posts go. The file format is important and must follow `YEAR-MONTH-DAY-title.MARKUP`. Permalinks can be customized in the post, but the date and markup language are determined by the filename.

- `_data`

  Well-formatted site data should go here. The Jekyll engine automatically loads all yaml files in this directory, meaning files ending in `.yml` or `.yaml`. If there is a `member.yml` file, its content can be accessed through `site.data.members`.

- `_site`

  Once Jekyll finishes conversion, the generated pages are placed here by default. It is best to put this directory into your `.gitignore`.

- `index.html` and other HTML, Markdown, and Textile files

  If these files contain YAML front matter, Jekyll will automatically convert them. Other files such as `.html`, `.markdown`, `.md`, or `.textile` in your site root or outside the directories mentioned above will also be converted.

- Other files and folders

  Other directories and files not mentioned, such as css, images, and favicon.ico, will be copied completely into the generated site.

Yes, this part borrows from the official Jekyll website because it has already explained the topic thoroughly. I do not want to repeat work unnecessarily.

In the next section, I will explain how to use each part with examples.

## Third-Party Services and Custom Configuration

### General Configuration

Open your Jekyll theme with your favorite text editor. First, edit `_config.yml`. Usually, it contains required SEO information and some of your personal information. Fill it according to your situation, and leave fields blank if you do not need them. Social links and default third-party services are usually configured here.

I do not think we need the posts that come only for demonstration. If you happen to use `Fedora with Gnome` like me, I suggest moving them to the `Templates` folder, so you can create new posts using their format.

Let us see how `.markdown(.md)` files for posts differ from ordinary files. Here is an example:

```markdown
---
title: Elements
description: Markdown-How-To
date: 2013-12-24 23:29:08
categories:
  - Foo
tags:
---

The purpose of this post is to help you make sure all of HTML elements can display properly. If you use CSS reset, don't forget to redefine the style by yourself.

---

# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

---

## Paragraph

Lorem ipsum dolor sit amet, [test link]() consectetur adipiscing elit. **Strong text** pellentesque ligula commodo viverra vehicula. *Italic text* at ullamcorper enim. Morbi a euismod nibh. <u>Underline text</u> non elit nisl. ~~Deleted text~~ tristique, sem id condimentum tempus, metus lectus venenatis mauris, sit amet semper lorem felis a eros.

Interdum et malesuada fames ac ante ipsum primis in faucibus. `Sed erat diam`, blandit eget felis aliquam, rhoncus varius urna.

> Praesent diam elit, interdum ut pulvinar placerat, imperdiet at magna.

## List Types

### Definition List

<dl><dt>Definition List Title</dt><dd>This is a definition list division.</dd></dl>

### Ordered List

1. List Item 1
2. List Item 2
3. List Item 3

### Unordered List

- List Item 1
- List Item 2
- List Item 3

## Table

| Table Header 1 | Table Header 2 | Table Header 3 |
| --- | --- | --- |
| Division 1 | Division 2 | Division 3 |
| Division 1 | Division 2 | Division 3 |
| Division 1 | Division 2 | Division 3 |
```

This article comes from the NexT theme and introduces basic Markdown usage. The content wrapped by a pair of `---` lines at the beginning belongs to YAML, containing document information such as title, description, category, tag, and date. I suggest adding this information to each article for record keeping.

You may also need to modify the content introducing the blogger. Some themes integrate this into `_config.yml`, while others include a document named `about/resume`. Replace its content with your own. Some themes use data in the `_data` folder or content introduced from `_include`; modify those as well. The syntax is simple, so I will not elaborate.

This lets you replace the information entirely with your own, but I suggest keeping part of the footer information because it usually declares which theme you are using.

### Third-Party Services

I am a little worried whether the description is clear enough. If you have any questions, contact me directly. This part introduces how to add third-party services.

Let us see what third-party services we may need:

1. Comments
   - Duoshuo
   - Disqus
   - Livere
2. Analytics/SEO
   - Baidu
   - Google

Here I use Livere and Google Analytics as examples. I choose them only because they are convenient; you can freely choose services that fit your situation.

#### Enabling the Google Analytics Plugin

Let us start with Google Analytics. It is usually well supported by different themes. All you need is to fill in the ID it provides. Of course, you need an independent domain for this, and you also need network access. If you want to use Baidu Analytics, you may need to file your domain, and Baidu's search engine seems to be on GitHub's blacklist.

Here I assume that you already have a domain and the required network access. If you need to register a domain, Tencent and Alibaba both provide services.

Open Google Analytics and follow the instructions. After completing all steps, you will get a string similar to `xx-xxxx-xxxx`. If not, find it from the provided Javascript code, then copy and paste it into the proper position in `_config.yml`.

Simple, right? This example mainly shows how such integrations work. Themes usually use Liquid conditionals to check whether `ga_track_id` is filled in `_config.yml`, then fill the corresponding id and domain into the right place.

This kind of code is usually located in `_include/footer.html`. In Huxblog, you can find `{% raw %}{% include footer.html %}{% endraw %}` in `_layout/default.html`, which includes `footer.html` in the page.

#### Installing the Livere Comment Plugin

I know this third-party comment system is not common, but considering the domestic environment, it is worth considering if you want to chat happily with friends.

Open livere.com and follow the registration and installation process. I do not want to describe these uninteresting steps too much. You will get a piece of js code.

- If you only plan to use it yourself, paste it directly into the appropriate position in `_layout/post.html`. This is usually the template used by your blog posts.
- If you want to make it into a plugin, I suggest creating `livere.html` in `_include` and pasting the code there. Replace the quoted content after `data-uid` with `{% raw %}{{ site.livere_uid }}{% endraw %}`. Then create a line `livere_uid: <your-data-uid>` in the appropriate position in `_config.yml`, and add `{% raw %}{% if site.livere_uid %}{{ include livere.html }}{% endif %}{% endraw %}` to `_layout/post.html`.
- If you want to control it through the front matter in blog `markdown` files, add it to `post.html` in the style of `{% raw %}{% if page.comments == true %}{% if site.livere_uid %}{{ include livere.html }}{% endif %}{% endif %}{% endraw %}`. Then you only need to add `comments: true` to the post front matter for it to work.

**I originally planned to discuss more, but I realized I had dragged this out for too long, and the methods are mostly similar. I will add more later if needed.**

## Publishing Your Page :)

Local preview is honestly not very interesting. Since it is only self-entertainment, publishing earlier is better, and you do not need to spend more time here with me.

You should still be able to find the `yourusername.github.io` repository you created at the beginning. Now we need to upload the content from your local `your-jekyll-theme` to that repository.

A very direct method is to click the repository's `Upload` button and drag all the content into it.

I think this is enough for you to complete the work. Enjoy your blog.

PS: If I now say that you can simply `fork` someone else's theme repository, rename the repository, modify the content, and get your own website, would you beat me up?
