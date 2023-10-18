# data = {'text':'hello', 'imgUrl':'/image.jpg', 'time':'2008'}
# innerHTML = '<div class="message message-left"><img src="{{ '+"url_for('static', filename='images/boy.png')"+' }}" alt="prominem"><div class="message-content"><p>'+data['text']+'</p><img src="'+data['imgUrl']+'" alt="图片缩略图" onclick="showImage('+"'"+data['imgUrl']+"'"+')"><span>'+data['time']+'</span></div></div>'
# print(innerHTML)

# # if __name__ == '__main__':
# #     app.run(debug=True, host='0.0.0.0', port=8080)

import os
current_path = os.path.dirname(os.path.abspath(__file__))
root_path = os.path.dirname(current_path)
print(root_path)