var UpdateBtns = document.getElementsByClassName('update-cart')


for(var i=0 ; i<UpdateBtns.length ;i++){

    UpdateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action= this.dataset.action
        console.log('productId',productId,'action',action)
        console.log('User',user)


        if(user === 'AnonymousUser'){

            addCookieItem(productId,action);
 }
  
        else{
            updateUserOrder(productId,action);
        }
    })
}



function addCookieItem(productId,action){
    console.log("user ")

    if(action == 'add'){
            if(cart[productId] == undefined){
                cart[productId] = { 'quantity' :1};

            }
            else{
                cart[productId]['quantity'] +=1 
            }
    }
    if(action == "remove"){
                cart[productId]['quantity'] -=1;

            
            if(cart[productId]['quantity'] <= 0){
                console.log("remove item")
                delete cart[productId]
            }
}
    console.log('Cart : ',cart)
    document.cookie = 'cart='+ JSON.stringify(cart)+ ";domain=;path=/"
    location.reload()

}



function updateUserOrder(productId,action){

    console.log("your logged ...")
    var url = '/updateItem/'

    fetch(url,{
        method : 'POST',
        headers :{
            'X-CSRFToken': csrftoken,
            'Content-Type' : 'application/json'
        },
        body : JSON.stringify({'productId': productId,'action':action})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data',data)
        location.reload()
    })
}

var viewProduct = document.getElementsByClassName('viewProduct')


for(var i=0 ; i<viewProduct.length ;i++){

    viewProduct[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action= this.dataset.action
        console.log('productId',productId,'action',action)
        console.log('User',User)

        if(User == 'AnonymousUser'){
            console.log("user is not logged")
        }
        else{
            viewProductFunc(productId,action);
        }
    })
}
function viewProductFunc(productId,action){

    console.log("your logged ...")
    var url = '/viewProduct/'

    fetch(url,{
        method : 'POST',
        headers :{
            'X-CSRFToken': csrftoken,
            'Content-Type' : 'application/json'
        },
        body : JSON.stringify({'productId': productId,'action':action})
    })
    .then((response)=>{
        return response.json()
    })
    .then((data)=>{
        console.log('data',data)
        
    })
}
function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}