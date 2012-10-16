
#Multiple Regression Analysis

neighborhoods<-read.table("Boston_Neighborhood_No_4_Neighborhoods_For_R.csv", header=T,sep=",")

#scatterplots
'plot(neighborhoods$article_count ~ neighborhoods$population , main="Boston Globe Articles & Neighborhood Population",ylab="Articles",xlab="Population")
abline(lm(neighborhoods$article_count ~ neighborhoods$population),col="blue")

plot(neighborhoods$article_count ~ neighborhoods$percent_non_white , main="Boston Globe Articles & % Non-White Population",ylab="Articles",xlab="% Non-White Population")
abline(lm(neighborhoods$article_count ~ neighborhoods$percent_non_white),col="blue")

plot(neighborhoods$article_count ~ neighborhoods$median_household_income , main="Boston Globe Articles & Median Household Income",ylab="Articles",xlab="Median Household Income")
abline(lm(neighborhoods$article_count ~ neighborhoods$median_household_income),col="blue")

plot(neighborhoods$article_count ~ neighborhoods$per_capita_income , main="Boston Globe Articles & Per Capita Income",ylab="Articles",xlab="Per Capita Income")
abline(lm(neighborhoods$article_count ~ neighborhoods$per_capita_income),col="blue")

plot(neighborhoods$article_count ~ neighborhoods$percent_unemployed , main="Boston Globe Articles & % Unemployed",ylab="Articles",xlab="% Unemployed")
abline(lm(neighborhoods$article_count ~ neighborhoods$percent_unemployed),col="blue")

plot(neighborhoods$article_count ~ neighborhoods$percent_below_poverty_level , main="Boston Globe Articles & % Below Poverty Level",ylab="Articles",xlab="% Below Poverty Level")
abline(lm(neighborhoods$article_count ~ neighborhoods$percent_below_poverty_level),col="blue")'

#multiple regression - standardized
myMultipleRegression = lm(scale(neighborhoods$article_count) ~ scale(neighborhoods$population) + scale(neighborhoods$percent_non_white) + scale(neighborhoods$median_household_income) + scale(neighborhoods$per_capita_income) + scale(neighborhoods$percent_unemployed) + scale(neighborhoods$percent_below_poverty_level))

#simple regression - standardized
mySimpleRegression=lm(scale(neighborhoods$article_count) ~ scale(neighborhoods$population))
#cor(x[c(1, 3, 10)])
cor(neighborhoods[c(1,2)], use="complete.obs", method="kendall")