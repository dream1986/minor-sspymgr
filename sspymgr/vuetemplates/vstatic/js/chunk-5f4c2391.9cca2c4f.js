(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-5f4c2391"],{a5a2:function(s,t,e){"use strict";e.r(t);var a=function(){var s=this,t=s.$createElement,e=s._self._c||t;return e("b-card",{staticClass:"rounded-0 text-left form-signin"},[e("b-card-header",[e("h3",{staticClass:"mb-0"},[s._v(s._s("Please Sign in"))])]),e("div",{staticClass:"card-body"},[e("form",{staticClass:"form needs-validation",attrs:{role:"form",autocomplete:"off",method:"post"}},[e("b-form-group",{attrs:{state:s.emailState}},[e("label",{staticClass:"sr-only",attrs:{for:"signinEmail"}},[s._v(s._s("Email address"))]),e("b-form-input",{staticClass:"form-control",attrs:{type:"email",id:"signinEmail",name:"email",required:"",autofocus:"",state:s.emailState},model:{value:s.email,callback:function(t){s.email=t},expression:"email"}}),e("b-form-invalid-feedback",[s.errors.email?e("div",[s._v(s._s(s.errors.email))]):e("div",[s._v(s._s("请填写正确的邮箱"))])])],1),e("b-form-group",{attrs:{state:s.passwordState}},[e("label",{staticClass:"sr-only",attrs:{for:"signinPassword"}},[s._v(s._s("Password"))]),e("b-form-input",{staticClass:"form-control",attrs:{type:"password",id:"signinPassword",name:"password",required:"",state:s.passwordState},model:{value:s.password,callback:function(t){s.password=t},expression:"password"}}),e("b-form-invalid-feedback",[s.errors.password?e("div",[s._v(s._s(s.errors.password))]):e("div",[s._v(s._s("请输入密码(至少 6 个字符)!"))])])],1),e("b-form-group",{staticClass:"mb-1"},[e("label",[e("b-form-checkbox",{attrs:{type:"checkbox",value:"remember-me",name:"keep_signedin"},model:{value:s.remember,callback:function(t){s.remember=t},expression:"remember"}},[s._v("\n            "+s._s("Remember me")+"\n          ")])],1)]),e("b-form-group",[e("span",{},[e("router-link",{attrs:{to:"/resetPassword"}},[s._v(s._s("Forget Password?"))])],1),e("span",{staticClass:"float-right"},[e("router-link",{attrs:{to:"/signup"}},[s._v(s._s("No Account?"))])],1)]),e("b-button",{staticClass:"btn-lg btn-block",attrs:{variant:"primary",type:"button"},on:{click:function(t){s.toSignIn()}}},[s._v("\n        "+s._s("Sign in")+"\n      ")]),e("p",{staticClass:"mt-5 mb-3 text-muted text-right"},[s._v("© 2017-2018")])],1)])],1)},r=[],i=(e("cadf"),e("551c"),e("097d"),e("8641")),n={name:"signin",data:function(){return{email:null,password:null,remember:!1,errors:{email:null,password:null,count:0}}},computed:{emailState:function(){return null===this.email?null:null===this.errors.email&&(this.email.indexOf("@")>0&&this.email.indexOf(".")>0)},passwordState:function(){return null===this.password?null:null===this.errors.password&&this.password.length>5}},methods:{toSignIn:function(){var s=this,t={email:this.email,password:this.password,keep_signedin:this.remember};this.errors.email=null,this.errors.password=null,Object(i["e"])(t).then(function(t){"fail"===t.status?(s.errors=t,s.errors.count=1):"success"===t.status&&("user"===t.level?window.location="/user":"admin"===t.level&&(window.location="/admin"))})}}},o=n,l=(e("b748"),e("2877")),m=Object(l["a"])(o,a,r,!1,null,null,null);m.options.__file="Signin.vue";t["default"]=m.exports},b748:function(s,t,e){"use strict";var a=e("d060"),r=e.n(a);r.a},d060:function(s,t,e){}}]);
//# sourceMappingURL=chunk-5f4c2391.9cca2c4f.js.map