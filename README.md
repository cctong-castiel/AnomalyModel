# AnomalyModel
- need to copy config.template.py and create config.py
- input and array of json with "comment_count", "share_count", "reaction_like" and undergo anomaly models to find out which post is out of the norm.

### pipe
- call /pipe
```
{
    "json_link": "https://abc.s3.amazonaws.com/folder/file.json"
}
```
- content structure in file.json
```
{
	"array_text": {
		"comment_count":[1,2,3,4,100,200,4,5,6,7],
		"share_count":[1,2,3,4,100,200,4,5,6,7],
		"reaction_like":[1,2,3,4,100,200,4,5,6,7],
		"post_timestamp": ["2020-06-01", "2020-06-02", "2020-06-03", "2020-06-04",
						   "2020-06-05", "2020-06-06", "2020-06-07", "2020-06-08",
				  		   "2020-06-09", "2020-06-10"],
		"live_sid": [1,2,3,4,5,6,7,8,9,10],
	  "post_message": ["1","2","3","4","5","6","7","8","9","10"]
	},
	"t_period": "D",
	"comment_f": null
}
```


return:
- an array of json with the data which is detected as anomal. 
 
