0. http://ec2-13-125-8-70.ap-northeast-2.compute.amazonaws.com:8500/

1. create folder
     ├── back_end/
     └── front_end/

2. init expo project
    $ expo init Dart

3. install Babel (Babel allows us to write next generation Javascript before it becomes the browser standard.)
    $ npm install @babel/core --save-dev

7. Install tools
    $ npm audit fix --legacy-peer-deps
    $ npm install react@latest react-dom@latest --save-dev --legacy-peer-deps
    $ npm install expo-notifications --save-dev
    $ npm install expo-splash-screen --save-dev
    $ npm install @react-navigation/native --save-dev  --legacy-peer-deps
    $ npm install @react-navigation/stack --save-dev --legacy-peer-deps
    $ npm install @react-navigation/bottom-tabs --save-dev --legacy-peer-deps
    $ npm install react-native-elements --save-dev  --legacy-peer-deps
    $ npm install expo-web-browser --save-dev --legacy-peer-deps
    $ npm install expo-auth-session expo-random --save-dev 
    $ npm install react-native-screens --save-dev --legacy-peer-deps
    $ npm install recyclerlistview --save-dev --legacy-peer-deps
    $ npm install victory-native --save-dev
    $ npm install react-native-gesture-handler --save-dev
    $ npm install react-native-text-avatar --save-dev
    $ npm install react-native-svg --save-dev  --legacy-peer-deps
    $ npm install expo-updates --save-dev
    $ npm install immer --save-dev

/*
4. make below file
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

5. Creating a Simple React App
    $ npm i react@latest react-dom@latest --save-dev

6. install Redux
    $ npm install redux react-redux redux-logger redux-thunk --save-dev

7. Install tools
    $ npm install @react-native-community/async-storage --save-dev
    $ npm install @react-navigation/bottom-tabs --save-dev
    $ npm install @react-navigation/native --save-dev
    $ npm install @react-navigation/stack --save-dev
    $ npm install expo-app-auth --save-dev
    $ npm install expo-auth-session --save-dev
    $ npm install expo-random --save-dev
    $ npm install jwt-decode --save-dev
    $ npm install react-google-charts --save-dev
    $ npm install react-native-elements --save-dev
    $ npm install react-native-screens --save-dev
    $ npm install react-native-text-avatar --save-dev
    $ npm install recyclerlistview --save-dev
    $ npm install victory-native --save-dev
    $ npm install react-native-gesture-handler --save-dev
    $ npm install @react-native-community/masked-view --save-dev
    $ npm install react-native-svg --save-dev
    $ npm install expo-splash-screen --save-dev
    $ npm install expo-secure-store --save-dev 
    $ npm install expo-notifications --save-dev 
    $ npm install expo-updates --save-dev 
*/

8. modify @react-navigation/routers/lib/module/index.js
    ref. https://stackoverflow.com/questions/60212460/how-to-remove-reach-navigation-5-x-warnings

9. run
    $ expo start

9.1 clear cache
    $ expo r -c

9.2 CORS문제
    chrome에서 플러그인 설치: Allow CORS: Access-Control-Allow-Origin

10. create key
    $ expo build:android --clear-credentials
    $ expo fetch:android:keystore

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
    $ sudo pip3 install flask_cors
    $ sudo pip3 install exponent_server_sdk

* google auth
    * web
        enabled Google Analytics API


        https://console.developers.google.com

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

* publish
    $ expo r -c
    $ expo publish
