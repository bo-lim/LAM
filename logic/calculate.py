def inputs_process(inputs):
    average_score = inputs[0]
    scores = inputs[1]
    students_score = list()
    for name, score in scores.items():
        students_score.append((name, score))
    random.shuffle(students_score)
    students_score = students_score[:5]
    processed_inputs = (average_score, students_score)
    return processed_inputs

class student:
    def __init__(self, name=""):
        self.name = name  # 이름
        self.score = 60  # 현재 점수
        self.reaction = 0  # 리액션 횟수
        self.score_list = list()  # 점수 기록

    # 1분당 1점씩 점수 감소
    def auto_minus(self):
        self.score -= 1

    # 리액션할 경우 점수 증가
    def React(self):
        self.score += 5
        if self.score > 100:
            self.score = 100
        self.reaction += 1  # 리액션 횟수 증가
        self.score_list.append(self.score)  # 점수 변화기록

    # 아무것도 안할 경우 점수만 기록
    def Nope(self):
        self.score_list.append(self.score)  # 점수 변화기록

    # 프레임에 없을 경우 점수 감소
    def OutofFrame(self):
        self.score -= 5
        if self.score < 0:
            self.score = 0
        self.score_list.append(self.score)  # 점수 변화기록

# Main function: 입력값을 학생 객체에 갱신시킨다.
def student_score_update(students_input):
    for name, result in students_input.items():
        student_in = False  # 매칭되는 학생 존재 여부
        # 만약 매칭되는 학생 개체가 있으면 갱신한다.
        for st in st_Obj_list:
            if name == st.name:
                student_in = True
                if result == 'clap' or result == 'nod' or result == 'smile':
                    st.React()
                elif result == 'default':
                    st.Nope()
                elif result == 'yawn' or result == 'outOfFrame':
                    st.OutofFrame()

        # 매칭되는 학생 개체가 없으면 생성한다.
        if student_in == False:
            st_Obj = student(name)
            st_Obj_list.append(st_Obj)
            if result == 'smile' or result == 'nod' or result == 'clap':
                st_Obj.React()
            elif result == 'default':
                st_Obj.Nope()
            elif result == 'outOfFrame' or result == 'yawn':
                st_Obj.OutofFrame()


def current_output():
    total_score = 0
    # 현재 수업 평균 점수 계산 및 기록 및 출력
    average_score = 60
    for st in st_Obj_list:
        total_score += st.score
    average_score = total_score / len(st_Obj_list)
    # 수업 평균 점수를 기록한다
    average_score_list.append(average_score)

    # student_output: {학생: 현재 점수, 학생: 현재 점수, 학생: 현재 점수}
    student_output = dict()
    for st in st_Obj_list:
        student_output[st.name] = st.score
    # 최종 out: (수업평균점수, student_output)
    return (average_score, student_output)


def final_output():
    # final_student_output: {학생: 평균 점수, 학생: 평균 점수, 학생: 평균점수}
    final_student_output = dict()
    for st in st_Obj_list:
        final_student_score = sum(st.score_list) / len(st.score_list)
        final_student_output[st.name] = (final_student_score, st.reaction)
    # 수업 전체 평균 점수
    final_class_score = sum(average_score_list) / len(average_score_list)
    # 최종 out: (final_student_output, 전체 최종 수업 평균, 수업 평균 점수 배열)
    return (final_student_output, final_class_score, average_score_list)


student_stat = {' ': (0, 0), ' ': (0, 0), ' ': (0, 0), ' ': (0, 0)}
