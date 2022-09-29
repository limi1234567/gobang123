'''
人机算法
'''


class GobangAlgorithm(object):
    def __init__(self, chessboard):
        self.chessboard = chessboard

    # 计算每个坐标点的对应棋子颜色的分数
    def get_point_score(self, x, y, color):
        '''

        :param x:水平方向
        :param y:垂直方向
        :param color:棋子颜色
        :return:每个点得分
        '''
        # 计算点周围5个子以内，空白和同色的分数
        blank_score = 0
        color_score = 0

        # 记录该点每个方向的棋子分数
        # 水平 垂直 正斜线 反斜线
        blank_score_plus = [0, 0, 0, 0]
        color_score_plus = [0, 0, 0, 0]
        # 水平方向
        # 右侧
        i = x  # 横坐标
        j = y  # 纵坐标
        while i < 19:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[0] += 1
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[0] += 1
            else:
                break
            if i >= x + 4:
                break
            i += 1
        # 左侧
        i = x
        j = y
        while i >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[0] += 1
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[0] += 1
            else:
                break
            if i <= x - 4:
                break
            i -= 1
        # 垂直方向
        # 下方
        i = x
        j = y
        while j < 19:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[1] += 1
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[1] += 1
            else:
                break
            if j >= y + 4:
                break
            j += 1
        # 上方
        i = x
        j = y
        while j >= 0:
            if self.chessboard[j][i] is None:
                blank_score += 1
                blank_score_plus[1] += 1
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[1] += 1
            else:
                break
            if j <= y + 4:
                break
            j -= 1
        # 正斜线
        # 右上
        i = x
        j = y
        while i < 19 and j >= 0:
            if self.chessboard[j][i] is None:
                blank_score_plus[2] += 1
                blank_score += 1
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[2] += 1
            else:
                break
            if i >= x + 4:
                break
            i += 1
            j -= 1
        # 左下
        i = x
        j = y
        while i >= 0 and j < 19:
            if self.chessboard[j][i] is None:
                blank_score_plus[2] += 1
                blank_score += 1
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[2] += 1
            else:
                break
            if j >= y + 4:
                break
            i -= 1
            j += 1
        #反斜线
        #右下
        i = x
        j = y
        while i < 19 and j < 19:
            if self.chessboard[j][i] is None:
                blank_score_plus[3] += 1
                blank_score += 1
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[3] += 1
            else:
                break
            if i >= x + 4:
                break
            i += 1
            j += 1
        #左上
        i = x
        j = y
        while i >= 0 and j >= 0:
            if self.chessboard[j][i] is None:
                blank_score_plus[3] += 1
                blank_score += 1
            elif self.chessboard[j][i] == color:
                color_score += 1
                color_score_plus[3] += 1
            else:
                break
            if i <= x - 4:
                break
            i -= 1
            j -= 1
        for k in range(4):
            #判断每个方向的同色棋子分数>=5,同色五子连珠
            if color_score_plus[k]>=5:
                return 100
        #获取指定位置的每条线上的总分，同色分数+空白分数返回最大分
        return max([x+y for x,y in zip(color_score_plus,blank_score_plus)])
    #获取位置坐标并返回
    def get_point(self):
        '''
        返回落子坐标
        :return:
        '''
        '''
        [
        [0,3,4,1,5],
        [1,2,0,5],
        [],
        []
        ]
        '''
        #初始化二维列表
        #存储黑棋，白棋每个坐标点的分数
        #白棋的每个坐标点的分数
        white_score=[[0 for i in range(19)] for j in range(19)]
        # 黑棋的每个坐标点的分数
        black_score = [[0 for i in range(19)] for j in range(19)]
        #测试落子，存储分数
        for i in range(19):
            for j in range(19):
                # 判断当前位置是否由棋子，无棋子返回空,
                if self.chessboard[i][j] !=None:
                    continue
                #模拟棋子 获得得分
                #测试白棋落子
                self.chessboard[i][j]='white'
                white_score[i][j]=self.get_point_score(j,i,'white')
                self.chessboard[i][j]=None
                # 测试黑棋落子
                self.chessboard[i][j] = 'Black'
                white_score[i][j] = self.get_point_score(j, i, 'Black')
                self.chessboard[i][j] = None
        #将二维坐标转化为一维坐标
        r_white_score=[]
        r_black_score=[]
        #列表的扩展
        # eg:old=[1,2,3] new[4,5,6]
         #
        for i in white_score:
            r_white_score.extend(i)
        for i in black_score:
            r_black_score.extend(i)
        print(r_white_score)
        print(r_black_score)
        #zip(r_white_score,r_black_score)=>[(0,0)(2,1)]
        #输出每个点位置分数最大值
        score =[max(x,y)for x,y in zip(r_white_score,r_black_score)]
        #找出分数最大值的下标
        chess_index=score.index(max(score))
        #输出x值坐标和y坐标
        #x坐标=下标取余
        #y坐标=下标取整
        x=chess_index%19
        y=chess_index//19
        return (x,y)



