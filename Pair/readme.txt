0. http://ec2-13-125-8-70.ap-northeast-2.compute.amazonaws.com:5000/

1. create folder
        ├── back_end/
        └── front_end/
            ├── static/
        │        ├── css/
        │        ├── js/
        │        ├── images/
        │        └── dist/
            └── templates/

2. init package manager to keep the project dependencies up to date, and to fetch and install new packages
    $ cd stock/analyzer/front_end
    $ sudo apt install curl software-properties-common
    $ curl -sL https://deb.nodesource.com/setup_12.x | sudo bash -
    $ sudo apt install nodejs
    $ npm init

3. install webpack. (It reduces the amount of modules my browser need to load, thereby decreasing the loading time of my webpages significantly for larger projects)
    $ npm i webpack webpack-cli --save-dev
    # To use webpack, we need to add a Webpack config file. The config tells webpack where to find the Javascript and React files, and where to put the generated Javascript bundle.

4. install Babel (Babel allows us to write next generation Javascript before it becomes the browser standard.)
    $ npm install --save-dev @babel/core @babel/preset-env babel-loader @babel/preset-react react-virtualized react-router-dom css-loader style-loader

5. make below file
    .babelrc
        {
          "presets": [
            "@babel/preset-env",
            "@babel/preset-react"
          ],
          "plugins": [
            "@babel/plugin-syntax-dynamic-import",
          ]
        }

6. Creating a Simple React App
    $ npm i react@latest react-dom@latest --save-dev

7. install Redux
    $ npm install redux react-redux --save-dev

8. install sass compiler
    $ npm install node-sass sass-loader --save-dev

9. Install tools
    $ npm install dayjs @date-io/dayjs --save-dev
    $ npm install redux-thunk redux-logger --save-dev
    $ npm install prop-types jest react-treebeard --save-dev
    $ npm install @material-ui/pickers --save-dev
    $ npm install @material-ui/icons@latest @material-ui/core@latest --save-dev
    $ npm install @emotion/styled @emotion/core --save-dev
    $ npm install react-virtualized-select react-swipeable-views  --save-dev
    $ npm install html-webpack-plugin clean-webpack-plugin --save-dev
    $ npm install filemanager-webpack-plugin --save-dev
    $ npm install react-loadable --save-dev

10. make below file
    webpack.config.js
        const webpack = require('webpack');

        const config = {
            entry:  __dirname + '/js/index.jsx',
            output: {
                path: __dirname + '/dist',
                filename: 'bundle.js',
            },
            resolve: {
                extensions: [".js", ".jsx", ".css"]
            },
            module: {
                rules: [
                    {
                        test: /\.jsx?/,
                        exclude: /node_modules/,
                        use: 'babel-loader'
                    }
                ]
            },
        };

        module.exports = config;


11. modify package.json
    "scripts": {
        "build": "webpack -p --progress --config webpack.config.js",
        "dev-build": "webpack --progress -d --config webpack.config.js",
        "test": "jest",
        "watch": "webpack --progress -d --config webpack.config.js --watch"
    },

12. run
    $ npm run dev-build

* control + F5
* ref)
    1. https://codeburst.io/creating-a-full-stack-web-application-with-python-npm-webpack-and-react-8925800503d9
    2. https://www.robinwieruch.de/minimal-react-webpack-babel-setup/
* mongoengin is too slow.... use PyMODM

* set localtime
    $ sudo mv /etc/localtime /etc/localtime_org
    $ sudo ln -s /usr/share/zoneinfo/Asia/Seoul /etc/localtime

* install hangul
    $ sudo apt-get install fonts-nanum*

* intall  mongodb - hikey
    $ sudo apt-get install mongodb

* intall  mongodb - CentOS ec2
    ref) https://docs.mongodb.com/manual/tutorial/install-mongodb-on-amazon/
    $ sudo vi /etc/yum.repos.d/mongodb-org.repo
        [mongodb-org-4.2]
        name=MongoDB Repository
        baseurl=https://repo.mongodb.org/yum/amazon/2/mongodb-org/4.2/x86_64/
        gpgcheck=1
        enabled=1
        gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc
    $ sudo yum install -y mongodb-org-4.2.1 mongodb-org-server-4.2.1 mongodb-org-shell-4.2.1 mongodb-org-mongos-4.2.1 mongodb-org-tools-4.2.1
    $ exclude=mongodb-org,mongodb-org-server,mongodb-org-shell,mongodb-org-mongos,mongodb-org-tools
    $ sudo service mongod start
    * its data file in /var/lib/mongo
    * its log file in /var/log/mongodb


* install python lib
    $ sudo apt install python3-pip
    $ sudo apt install pkg-config
    $ sudo apt install libfreetype6-dev
    $ sudo apt install liblapack-dev
    $ sudo pip3 install flask-restful
    $ sudo pip3 install requests apscheduler
    $ sudo pip3 install python-dateutil
    $ sudo pip3 install pandas
    $ sudo pip3 install matplotlib
    $ sudo pip3 install libblas-dev statsmodels
    $ sudo pip3 install pymongo pymodm
    $ sudo pip3 install pyjwt objgraph xlsxwriter aiohttp

* docker mongodb
    $ systemctl daemon-reload
    $ sudo service docker restart
    $ sudo service docker status (should see active (running))
    $ sudo docker run rpi3-mongodb3

* mongodb shell
    $ show dbs
    $ use stock_analyzer
    $ show collections
    $ db.pair.node.aggregate([{$group:{_id:"$date2",max_date:{$max:"$date2"}}}])

* mongodb error (=>Pymongo keeps refusing the connection at 27017)
    => hikey
    $ sudo rm /var/lib/mongodb/mongod.lock
    $ sudo service mongodb start

* mongodb error (=>Pymongo keeps refusing the connection at 27017)
    => aws
    $ sudo rm /var/lib/mongo/mongod.lock
    $ sudo service mongod start

* config
    $ cat /etc/mongodb.conf

* rest api
    curl -X GET http://url
    curl -X PUT -H "Content-Type: application/json" -d '{"name":"s"}' http://url
    curl POST -H "Content-Type: application/json" -d '{"name":"s"}' http://url
    curl -X DELETE -H "Content-Type: application/json" -d '{"name":"s"}' http://url

* systemd (/etc/systemd/system/stock_analyzer.service)
    $ systemctl daemon-reload
    $ systemctl enable stock_analyzer

    [Unit]
    Description=Execute Stock Analyzer Server
    After=network-online.target
    Wants=network-online.target

    [Service]
    User=yepark
    Type=idle
    ExecStartPre=/bin/sleep 10
    ExecStart=/home/yepark/Production/stock_analyzer/tmux_run.sh
    RemainAfterExit=true
    Restart=on-failure

    [Install]
    WantedBy=multi-user.target


git clone https://github.com/miraclehand/stock_analyzer.git
git status
git add *
git commit -m ""
git remote -v
git push origin master
git pull origin master

