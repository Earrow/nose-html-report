# nose-html-report

为nose创建html报告的插件。

安装：
```
python setup.py install
```

用法：
```
nosetests --with-html --html-file=report.html --html-title=测试报告
```

效果示例：
![image](https://github.com/Earrow/nose-html-report/blob/master/images/001.png)


插件参考了[nose2-html-report](https://github.com/mgrijalva/nose2-html-report)和[nose-html-output](https://github.com/openstack-infra/nose-html-output)，将nose2-html-report的报告模板移植到nose。
