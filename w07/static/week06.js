//大改1-4_1抓取屬性中的資料回填到姓名
let nameContent=document.getElementById("getName").getAttribute("d");
let nameBlock = document.createElement("div");     //创建一个div元素
let result_Name=document.createTextNode(nameContent+"歡迎登入系統");
nameBlock.appendChild(result_Name);
nameBlock.setAttribute("class","mid");
document.getElementById("getName").appendChild(nameBlock);



//處理歷史訊息
// 取得資料
let historyContent=document.getElementById("getHistory").getAttribute("d");
// console.log(historyContent);
//整理成陣列
let historyContent2=historyContent.replaceAll("(","").replaceAll(")","").replaceAll("[","").replaceAll("]","").replaceAll("'","")
// console.log(historyContent2);
let historyContent3=historyContent2.split(",");
// console.log(historyContent3);
// 取得陣列長度
// console.log(historyContent3.length);
// console.log(historyContent3[0]+historyContent3[1]);

// let a="";
// console.log(a.length);
// console.log(historyContent3[0]+historyContent3[1]);
if (historyContent3.length >1){
    let arrayLen=historyContent3.length
    for(let i =0;i<arrayLen/2;i++){
        let historyBlock = document.createElement("div");     //创建一个div元素
        let result_history=document.createTextNode(historyContent3[2*i]+" : "+historyContent3[1+2*i]);
        historyBlock.appendChild(result_history);
        historyBlock.setAttribute("class","mid");
        document.getElementById("getHistory").appendChild(historyBlock);    
    }
}


// searchname
let searchname_input = document.querySelector("#searchname_input");
let searchname_botton = document.querySelector("#searchname_botton");
// 觸發searchname事件
function submitBtn() {
    let username = searchname_input.value;
    fetch("/api/member?username="+String(username))
    .then((res) => {
        const data = res.json();
        return data;
    })
    .then((data) => {
        console.log(data["data"]);
        if(data["data"] != null){
            let el = document.querySelector("#get_searchname");
            console.log(el);
            el.setAttribute("class","mid");
            el.textContent = data["data"]["name"];
        }
        else{
            let el = document.querySelector("#get_searchname");
            el.setAttribute("class","mid");
            el.textContent = null;
        }
    });
}
searchname_botton.addEventListener("click", submitBtn);



//1.前端事件姓名更新紐按下後去抓輸入欄的new_name，接著用PATCH方法把new_name包在body
//2.後端透過request.get_json() #透過JS抓到在HTML輸入的新的名字，確認更改後，return回/api/member
//3.前端如何設定另一個事件再次抓取/api/member的值?不需要
function submit_update(){
    let updatename=document.querySelector("#updatename_input");
    // // console.log("updatename: ",updatename);
    // if (updatename.value){
    //     new_name={
    //         "name":updatename.value
    //     }
    // // console.log("準備出事");
    // // console.log(new_name);
    //     fetch("/api/member/",{
    //         method:"PATCH",
    //         credentials:"include",
    //         body:JSON.stringify(new_name), //使用patch方法傳遞到前端
    //         cache:"no-cache",
    //         headers:new Headers({
    //             "content-type":"application/json"
    //         })
    //     })
    //     .then(function(update_connect){
    //         if(update_connect.status !== 200){
    //             console.log("Response status was not 200",update_connect.status)
                
    //         }
    //         console.log("未JSON:",update_connect)
    //         // console.log("update_connect:",update_connect.json());
    //         return update_connect.json()
    //     })
    //     .then(function(data_json){
    //         //"ok" in data_json
    //         console.log("data_json",data_json);
    //         if (data_json.hasOwnProperty("ok")){
    //             let block_name=document.querySelector("#getName");
    //             block_name.setAttribute("class","mid");
    //             block_name.innerHTML = updatename.value+" 歡迎登入系統";
    //             let name_state=document.querySelector("#get_updatename");
    //             name_state.setAttribute("class","mid");
    //             name_state.innerHTML = "更新成功";

    //         }

    //     })
    //     }

    new_name={
            "name":updatename.value
        }
    console.log("準備出事");
    console.log(new_name);
    fetch("/api/member/",{
        method:"PATCH",
        credentials:"include",
        body:JSON.stringify(new_name), //使用patch方法傳遞到前端
        cache:"no-cache",
        headers:new Headers({
            "content-type":"application/json"
        })
    })
    .then(function(update_connect){
        if(update_connect.status !== 200){
            console.log("Response status was not 200",update_connect.status)
            
        }
        console.log("未JSON:",update_connect)
        // console.log("update_connect:",update_connect.json());
        return update_connect.json()
    })
    .then(function(data_json){
        //"ok" in data_json
        console.log("data_json",data_json);
        if (data_json.hasOwnProperty("ok")){
            let block_name=document.querySelector("#getName");
            block_name.setAttribute("class","mid");
            block_name.innerHTML = updatename.value+" 歡迎登入系統";
            let name_state=document.querySelector("#get_updatename");
            name_state.setAttribute("class","mid");
            name_state.innerHTML = "更新成功";

        }

    })
}






    //再fetch一次判斷是否改名成功後方可使用
    // let original_name=document.querySelector("#getName");
    // original_name.innerHTML = name.value+" 歡迎登入系統";
    // original_name.setAttribute("class","mid");
    // console.log(original_name);

    








// // 事件監聽器
// let button= document.querySelector("#more_message")
// button.addEventListener("click",function(){
    // let node = document.createElement("div");
    // let textnode = document.createTextNode("WaterWaterWaterWater");
    // node.appendChild(textnode);
    // document.getElementById("myList").appendChild(node);
    // console.log("onclick");

// })


// let historyContent=document.getElementById("getHistory").getAttribute("d");
//整理資料作轉態
// historyContent=historyContent.replaceAll("(","").replaceAll(")","").replaceAll('[','"').replaceAll(']','"')
// historyContent=JSON.parse(historyContent)
// console.log(historyContent[1]);
// historyContent2=historyContent.replaceAll("(","").replaceAll(")","").replaceAll("[","").replaceAll("]","")
// historyContent2=historyContent.replaceAll("(","").replaceAll(")","").replaceAll("[","").replaceAll("]","").replaceAll("'","")
// len=historyContent2.length
// console.log(len);
// console.log(historyContent2.substr(0, len-2));




// let historyBlock = document.createElement("div");     //创建一个div元素
// let result_history=document.createTextNode(historyContent);
// historyBlock.appendChild(result_history);
// historyBlock.setAttribute("class","mid");
// document.getElementById("getHistory").appendChild(historyBlock);



// var data = "0,1,2,3";
// var arr = JSON.parse("[" + data + "]");
// console.log(arr);

// let nameContent=document.getElementById("getName").getAttribute("d");
// let result=document.createTextNode(num**2);
// nameBlock.appendChild(result);
// nameBlock.setAttribute("class","mid");
// document.getElementById("flagEnd").appendChild(nameBlock);
// console.log(num.replaceAll("(","[").replaceAll(")","]"));
// num = num.replaceAll("'",'"')
// ------console.log(JSON.stringify(num))
// let num2=JSON.parse(num);
// console.log(num2["peopleNow"]);

// // 事件監聽
// let button= document.querySelector("#searchname_botton")
// button.addEventListener("click",function(){
//     // 取得資料
//     let search_name=document.querySelector("#searchname_input")
//     // let node = document.createElement("div");
//     // let textnode = document.createTextNode("WaterWaterWaterWater");
//     // node.appendChild(textnode);
//     // document.getElementById("myList").appendChild(node);
//     console.log("onclick");
//     console.log(search_name.value);

//     // fetch("http://127.0.0.1:3000/api/member/?username=111")
//     // .then((res) => {
//     //     const data = res.json();
//     //     return data;
//     // })
//     // .then((data) => {
//     //     console.log(data);
//     // });

// })
