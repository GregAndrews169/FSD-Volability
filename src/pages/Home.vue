<template>
    <div class="container-fluid p-5">
        <!-- Top Section -->
        <div class="text-center my-5">
            <h1 class="font-weight-bold mb-4">Advanced Crypto Analytics</h1>
            <h2 class="font-weight-bold mb-4">Start your Journey to Market Mastery with Volability </h2>
            <h3 class="mb-4">Unlock  Powerful Market Insights </h3>


        </div>

        <div class="row mt-5">
            <!-- First Block: Time Series  -->
            <div class="blocks" style="float: left; width: 32%;">
                <div class="p-4"
                    style="border: 3px solid #e0e0e0; border-radius: 10px; margin-top: 50px; margin-right:20px;">
                    <h3 class="heading-styling">Time Series Analysis</h3>
                    <p style="margin-left: 10px; margin-right:10px">
                        Harness the power of time series analysis to identify and capitalize on market trends. Our tools
                        enable retail investors to track historical price movements and forecast future patterns, creating
                        opportunities for strategic investment decisions.
                        <br>
                        <br>
                        <router-link to="/" class="links">Start Time Series Analysis ></router-link>


                    </p>
                </div>
            </div>
            <!--Second Block: Correlation -->
            <div class="blocks" style="float: left; width: 32%;">
                <div class="p-4"
                    style="border: 3px solid #e0e0e0; border-radius: 10px; margin-top: 50px; margin-right:20px;">
                    <h3 class="heading-styling">Static Analysis</h3>
                    <p style="margin-left: 10px; margin-right:10px">
                        Dive into the comprehensive static analysis to evaluate the scale and liquidity of your crypto
                        assets. Our analytics offer crucial insights that help you refine your asset selection and
                        investment strategy. Gain a clearer understanding of the market to make well-informed decisions that
                        align with your investment goals.



                        <br>
                        <br>

                        <router-link to="/StaticAnalysis" class="links">Start Static Analysis ></router-link>

                    </p>
                </div>
            </div>
            <!-- Third Block: Correlation analysis -->
            <div class="blocks" style="float: left; width: 32%;">
                <div class="p-4"
                    style="border: 3px solid #e0e0e0; border-radius: 10px; margin-top: 50px; margin-right:20px;">
                    <h3 class="heading-styling">Correlation Analysis</h3>
                    <p style="margin-left: 10px; margin-right:10px">

                        Unveil the hidden relationships between crypto assets with our correlation analysis tools. By
                        understanding these dynamics, you can build a diversified portfolio that is resilient against market
                        volatility and contagion effects.
                        <br>
                        <br>
                        <router-link to="/Correlation" class="links">Start Static Analysis ></router-link>



                    </p>
                </div>
            </div>
        </div>

        <!-- Profit & Loss block -->
        <div class="blocks" style="float: left; width: 96%;">
            <div class="p-4" style="border: 3px solid #e0e0e0; border-radius: 10px; margin-top: 50px; margin-right:20px;">
                <h3> Advanced Portfolio Analysis </h3>
                <p style="margin-left: 15px; margin-right:15px">

                    Take control of your cryptocurrency investments with our comprehensive Profit and Loss Assessment tool.
                    Input your transaction details to track the performance of your assets over time. Our platform
                    calculates your gains or losses, taking into account factors like purchase price, current value, and
                    fees, to provide a clear picture of your investment journey.
                    <br>


                    <router-link to="/PnL" class="button-link">
                        <button
                            style="padding: 20px 50px; margin-right: 50px; margin-top: 30px; background-color: #9746D6; color: white">
                            Analyse my Portfolio
                        </button>
                    </router-link>
                </p>
            </div>
        </div>

    </div>
</template>
  


  
<style scoped>
.heading-styling {
    color: hsl(274, 92%, 75%);
}

.links {
    color: hsl(274, 92%, 75%);
}
</style>