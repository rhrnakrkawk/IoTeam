<script>
  let food_list = {};
  let total_sales = 0;
  function get_food_list() {
    fetch("http://127.0.0.1:8000/food").then((response) => {
      response.json().then((json) => {
        console.log(json);
        food_list = json;
        food_list = JSON.parse(JSON.stringify(food_list));
        console.log(food_list["1"]["price"]);
      });
    });
  }

  function get_total_sales() {
    fetch("http://127.0.0.1:8000/sales").then((response) => {
      response.json().then((json) => {
        total_sales = json;
      });
    });
  }

  get_food_list();
  get_total_sales();
</script>

<h1>현재 등록된 음식 목록</h1>

{#if food_list === "No Food"}
  <p class="nofood">등록된 음식이 없습니다.</p>
{:else}
  <ol>
    {#each Object.keys(food_list) as food}
      <li>이름 : {food}, 가격 : {food_list[food]["price"]}</li>
    {/each}
  </ol>
{/if}

<h1>오늘의 매출</h1>
<p>{total_sales}원 입니다.</p>

<style>
  h1 {
    text-align: center;
    width: auto;
  }
  ol {
    text-align: left;
    width: auto;
  }
  li {
    font-style: normal !important ;
    font-size: 20px;
    margin: 10px;
  }
  .nofood {
    text-align: center;
    font-weight: bold;
    font-display: block;
    font-size: 20px;
    margin: 100px;
  }
  p {
    text-align: center;
    font-weight: bold;

    font-size: 20px;
  }
</style>
