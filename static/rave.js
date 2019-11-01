new Vue({
    el: '#app',
    components:{
      'Rave': VueRavePayment.default
    },
    computed: {
        reference(){
          let text = "";
          let possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
 
          for( let i=0; i < 10; i++ )
            text += possible.charAt(Math.floor(Math.random() * possible.length));
 
          return text;
        }
    },
    methods: {
      callback: function(response){
        console.log(response)
      },
      close: function(){
        console.log("Payment closed")
      }
    },
    data: {
      raveBtnText: "Pay Me, My Money",
      raveKey: "FLWPUBK-xxxxxxxxxxxxxxxxx-X",
      email: "foobar@example.com",
      amount: 10000
    }
});