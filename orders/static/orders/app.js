$(document).ready(function() {
    $(document).on("keyup", function(e) {
        if (e.keyCode === 27) {
            $(".popUpWin").hide()
            $(".popUpWinContentA").hide()
            $(".popUpWinContentB").hide()
            $(".popUpWinContentC").hide()
            $(".popUpWinContentD").hide()
            $(".topping1").hide()
            $(".topping2").hide()
            $(".topping3").hide()
            $(".cheese").hide()
            $(".subAddOn").hide()
        }
    })
    $(".popUpWin").hide()
    $(".popUpWinContentA").hide()
    $(".popUpWinContentB").hide()
    $(".popUpWinContentC").hide()
    $(".popUpWinContentD").hide()
    $(".topping1").hide()
    $(".topping2").hide()
    $(".topping3").hide()
    $(".cheese").hide()
    $(".subAddOn").hide()
    $(".closeButton").on("click", function() {
        $(".popUpWin").hide()
        $(".popUpWinContentA").hide()
        $(".popUpWinContentB").hide()
        $(".popUpWinContentC").hide()
        $(".popUpWinContentD").hide()
        $(".topping1").hide()
        $(".topping2").hide()
        $(".topping3").hide()
        $(".cheese").hide()
        $(".subAddOn").hide()

    })
    // $(".alert.alert-success").delay(3000).fadeOut()
});

function popUpA(category, item_name, item_price, item_size, add_on){
    $("#priceSpan").html(parseFloat(item_price).toFixed(2))
    $(".subAddOn").html("");
    $(".popUpWin").show();
    $(".popUpWinContentA").show();
    $("#popUpWinTitle").html(category+"<br>"+item_name)
    $(".inviForm").html(`
        <input type="hidden" name="name" value="${item_name}">
        <input type="hidden" name="price" value="${item_price}">
        <input type="hidden" name="size" value="${item_size}">
        `)
    if (category=="Regular Pizza"||category=="Sicilian Pizza") {
        for (x=1; x<=3; x++) {
            for (i in add_on) {
                var opt = $("<option></option>");
                opt.val(add_on[i].name);
                opt.html(add_on[i].name);
                $(`select[name=topping${x}]`).append(opt);
            }
            opt = $("<option hidden selected value=''>Please select</option>")
            $(`select[name=topping${x}]`).append(opt);
        }
        if (~item_name.indexOf("1 topping")) {
            $(".topping1").show()
        }
        if (~item_name.indexOf("2 topping")) {
            $(".topping1").show()
            $(".topping2").show()
        }
        if (~item_name.indexOf("3 topping")) {
            $(".topping1").show()
            $(".topping2").show()
            $(".topping3").show()
        }
    }
    else if (category=="Subs") {
        for (i in add_on) {
            i=parseInt(i)
            var input= $(`<input type="checkbox" name="add_on${i+1}" value="${add_on[i].name}" onclick=updatePrice(${add_on[i].price},"add_on${i+1}")>`)
            var label = $(`<label>${add_on[i].name} </label>`)
            label.append(input)
            $(".subAddOn").append(label)
            $(".subAddOn").append("<br>")
        }
        var input= $(`<input type="checkbox" name="cheese" value="yes" onclick=updatePrice(0.5,"cheese")>`)
        var label = $(`<label>Extra cheese? </label>`)
        label.append(input)
        $(".subAddOn").append(label)
        $(".subAddOn").append("<br>")
        $(".cheese").show()
        $(".subAddOn").show()
        if (~item_name.indexOf("Steak")) {
            $(".addOn1").show()
            $(".addOn2").show()
            $(".addOn3").show()
        }
    }
    else {
        for (x=1; x<=3; x++) {
            opt = $("<option hidden selected value=''>Please select</option>")
            $(`select[name=topping${x}]`).append(opt);
        }
    }
}

function popUpB(user_cart,total) {
    $(".orderReview").html("")
    $(".popUpWin").show()
    $(".popUpWinContentB").show()
    $("#popUpWinTitleB").html("Confirm Order?")
    for (var i in user_cart) {
        const item = $(`<p>${user_cart[i].category} | ${user_cart[i].item} | Price: ${user_cart[i].price}</p>`)
        $(".orderReview").append(item)
    }
    const p = $(`<p>Your total: ${total.toFixed(2)}</p>`)
    $(".orderReview").append(p)
}

function popUpC(category, item, price) {
    $(".popUpWin").show()
    $(".popUpWinContentC").show()
    $("#popUpWinTitleC").html("Confirm Delete?")
    $(".inviForm").html(`
        <input type="hidden" name="category" value="${category}">
        <input type="hidden" name="item" value="${item}">
        <input type="hidden" name="price" value="${price}">
    `)
    const p = $(`<p>${category} | ${item}</p>`)
    $(".removeReview").html(p)
}

function popUpD() {
    $(".popUpWin").show()
    $(".popUpWinContentD").show()
    $("#popUpWinTitleD").html("Register")
    $("#registerUsername").focus()
}

function updatePrice(data,data1) {
    var total = parseFloat($("#priceSpan").html())
    var checkBox = $(`input[name="${data1}"]`)
    if (checkBox[0].checked == true) {
        total += parseFloat(data)
    }
    else {
        total -= parseFloat(data)
    }
    $("#priceSpan").html(total.toFixed(2))
    $("input[name='price']").val(total.toFixed(2))
}

function orderReady(order_number,order_cart) {
    $(".popUpWinContentAsub").html("")
    for (var i in order_cart) {
        if (order_cart[i].order_number_id==order_number) {
            var div = $("<div></div>")
            var item = $(`<p>${order_cart[i].category} | ${order_cart[i].item} | ${order_cart[i].price}</p>`)
            div.append(item)
            $(".popUpWinContentAsub").append(div)
        }
    }
    $(".popUpWin").show()
    $(".popUpWinContentA").show()
    $(".inviForm").html(`
        <input type=hidden name="order_number" value="${order_number}">
    `)

}

function orderDetails(order_number,order_cart) {
    $(".popUpWinContentA").html("")
    for (var i in order_cart) {
        if (order_cart[i].order_number_id==order_number) {
            var div = $("<div></div>")
            var item = $(`<p>${order_cart[i].category} | ${order_cart[i].item} | ${order_cart[i].price}</p>`)
            div.append(item)
            $(".popUpWinContentA").append(div)
        }
    }
    $(".popUpWin").show()
    $(".popUpWinContentA").show()
}
