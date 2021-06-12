<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/ozyildirim/cmk-checker">
    <img src="CMK.png" alt="Logo" width="320" height="320">
  </a>
  <h3 align="center">CMK Checker</h3>
  <p align="center">
    Static Code Smell Detector for Unity Games
    <br />
    <a href="https://github.com/ozyildirim/cmk-checker"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ozyildirim/cmk-checker">View Demo</a>
    ·
    <a href="https://github.com/ozyildirim/cmk-checker/issues">Report Bug</a>
    ·
    <a href="https://github.com/ozyildirim/cmk-checker/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

The project that explained below is aims to help developers to figure out problems in their Unity source codes. CMK Checker is static code analyze tool for games which is created in Unity and written in C# programming language. Tool checks source code and log the results to developer. Tool can find 8 differen types of code smell that can affect Unity games.


### Built With

* Python




<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* python
* lxml
  ```sh
  pip install lxml
  ```
* srcML
  ```sh
  https://www.srcml.org/
  ```



### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/ozyildirim/cmk-checker.git
   ```


<!-- USAGE EXAMPLES -->
## Usage

CMK Checker is command line based tool. It is open-source available to improve.

## If you just want to tool for analyzing source codes

1. Change your directory into CMK Checker.
   <img src="images\ss1.png">
2. Depict source code directory and run checker with that.
   <img src="images\ss2.png" width= "5500" height="40">

3. Analyze results will be shown in command line. Detailed logs will be also exported into log_txt_file.txt which is located in tool's directory.
   <img src="images\ss3.png">
   
## You can also add new checking rules easily, tool is splitted into different modules.

In checker.py, you can see that algorithms are written by using libraries like "minidom,lxml". You can specify your own rule and use it easily. after implementation of search function, you must add it into StartChecker function.





<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Ömer Kutay YILDIRIM - yildirimkutay@outlook.com.tr

Can ÖZCAN - canozcantr@gmail.com

Mazlum Ferhat KAYA - mazlumky@gmail.com

Project Link: [https://github.com/ozyildirim/cmk-checker](https://github.com/ozyildirim/cmk-checker)






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/github_username
