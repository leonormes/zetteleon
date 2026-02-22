# GitHub - danielgatis/imgcat: Display images and gifs in your terminal.

![rw-book-cover](https://opengraph.githubassets.com/96b0a32691f636186595288577665b1dc6fe78ae20e5ef39e89e9238779ff81e/danielgatis/imgcat)

## Metadata
- Author: [[https://github.com/danielgatis/]]
- Full Title: GitHub - danielgatis/imgcat: Display images and gifs in your terminal.
- Category: #articles
- Summary: Imgcat is a tool that shows images and GIFs inside your terminal. It works on Mac, Linux, and Windows and supports animated GIFs and transparency. You can install it easily and use simple commands to display pictures from your computer or the internet.
- URL: https://github.com/danielgatis/imgcat

## Full Document
### danielgatis/imgcat

Open more actions menu

### Imgcat

[![Go Report Card](https://camo.githubusercontent.com/b2a2c60d0d317b6b477ebb020f56590cd4e7d06ea039c85098c9bd5af92b96f5/68747470733a2f2f676f7265706f7274636172642e636f6d2f62616467652f6769746875622e636f6d2f64616e69656c67617469732f696d676361743f7374796c653d666c61742d737175617265)](https://goreportcard.com/report/github.com/danielgatis/imgcat)
[![License MIT](https://camo.githubusercontent.com/6581c31c16c1b13ddc2efb92e2ad69a93ddc4a92fd871ff15d401c4c6c9155a4/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d4d49542d626c75652e737667)](https://raw.githubusercontent.com/danielgatis/imgcat/master/LICENSE)
[![Go Doc](https://camo.githubusercontent.com/fe1188b9f0668a1e0a543e1cbcc6fb28d50a52f74d04e99407f8e6405a7132cd/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f676f646f632d7265666572656e63652d626c75652e7376673f7374796c653d666c61742d737175617265)](https://godoc.org/github.com/danielgatis/imgcat)
[![Release](https://camo.githubusercontent.com/88681948290d19913d6c0f8bc5a70a2f742de8531607ebe4ab62afc1e3856fbc/68747470733a2f2f696d672e736869656c64732e696f2f6769746875622f72656c656173652f64616e69656c67617469732f696d676361742e7376673f7374796c653d666c61742d737175617265)](https://github.com/danielgatis/imgcat/releases/latest)
Display images and gifs in your terminal emulator.

[![](https://github.com/danielgatis/imgcat/raw/master/demo.gif)](https://github.com/danielgatis/imgcat/blob/master/demo.gif)
  [![demo.gif](https://github.com/danielgatis/imgcat/raw/master/demo.gif)](https://github.com/danielgatis/imgcat/blob/master/demo.gif)  

##### Features

* Animated GIF support
* Accept media through stdin
* Transparency

##### Installation

###### MacOS

```
brew install danielgatis/imgcat/imgcat

```

###### Linux

First, [install snapcraft](https://snapcraft.io/docs/installing-snapd).

```
sudo snap install imgcat

```

###### Windows

First, [install scoop](https://github.com/lukesampson/scoop#installation).

```
scoop bucket add scoop-imgcat https://github.com/danielgatis/scoop-imgcat.git
scoop install scoop-imgcat/imgcat

```

###### Download binaries

Alternatively, you can download a pre-built binary [here](https://github.com/danielgatis/imgcat/releases).

##### Build from source

First, [install Go](https://golang.org/doc/install).

Next, fetch and build the binary.

```
go install github.com/danielgatis/imgcat@latest
```

or, if you use pre-1.17 Go version, use the `go get` command:

```
go get -u github.com/danielgatis/imgcat
```

##### Usage

Display a remote image

```
curl -s http://input.png | imgcat

```

Display a local image

```
imgcat path/to/image.png

```

###### Options

* `-h`, `-help`: Show help message
* `-interpolation`: Set interpolation method (default: `lanczos`)
	+ `nearest`: Fastest resampling filter, no antialiasing.
	+ `lanczos`: A high-quality resampling filter for photographic images yielding sharp results.
* `-silent`: Hide Exit message (default: false).
* `-top-offset`: Offset from the top of the terminal to start rendering the image (default 8)
* `-type`: Image resize type. Options: fit, resize (default "fit")

##### Requirements

Your terminal emulator must be support `true color` and use a `monospaced font` that includes the lower half block unicode character (`▄ U+2584`).

##### License

Copyright (c) 2020-present [Daniel Gatis](https://github.com/danielgatis)

Licensed under [MIT License](https://github.com/danielgatis/imgcat/blob/master/LICENSE)

##### Buy me a coffee

Liked some of my work? Buy me a coffee (or more likely a beer)

[![Buy Me A Coffee](https://camo.githubusercontent.com/4c31625833b2598a9acf63a0a82416a0621a93d5d4f5aa285eef92593e5ebc42/68747470733a2f2f626d632d63646e2e6e7963332e6469676974616c6f6365616e7370616365732e636f6d2f424d432d627574746f6e2d696d616765732f637573746f6d5f696d616765732f6f72616e67655f696d672e706e67)](https://www.buymeacoffee.com/danielgatis)
