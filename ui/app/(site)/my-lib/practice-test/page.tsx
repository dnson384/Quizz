"use client";
import Header from "@/presentation/components/Layout/Header";
import SideMenu from "@/presentation/components/Layout/SideMenu";

import SingleChoice from "../../../../presentation/components/MyLib/PracticeTest/SingleChoice";
import MultipleChoice from "../../../../presentation/components/MyLib/PracticeTest/MultipleChoice";

import useMyPractice from "@/presentation/hooks/MyLib/useUserPracticeTest";
import TrueFalse from "../../../../presentation/components/MyLib/PracticeTest/TrueFalse";

export default function MyPracticeTest() {
  const {
    // Data
    baseInfo,
    questions,
    changedName,
    changedQuestions,
    deleteOptions,
    deleteQuestions,
    // UI
    isSubmitted,
    // Card Behavior
    handleAddCard,
    handleDeleteCard,
    // Input Change
    handleBaseInfoChange,
    handleQuestionChange,
    handleAddOption,
    handleDeleteOption,
    // Save
    handleSaveChange,
    handleDeletePracticeTest,
  } = useMyPractice();

  const titleMissing =
    changedName === undefined ||
    changedName.name.length === 0 ||
    changedName.name === baseInfo?.name;
  const anyMissing = changedQuestions.some((changeQuestion) => {
    if (changeQuestion.question?.text.length === 0) return true;
    const isOptionTextMissing = changeQuestion.options.some(
      (changeOption) => changeOption.text.length === 0,
    );
    if (isOptionTextMissing) return true;

    const hasAnswerOption = changeQuestion.options.some(
      (option) => option.isCorrect === true,
    );
    if (!hasAnswerOption) return true;
  });
  const isFormValid = !titleMissing || (!anyMissing && changedQuestions.length > 0);

  return (
    <>
      <Header />

      <main className="flex">
        <SideMenu />
        <section className="mt-[74px] w-6xl mx-auto">
          <div className="sticky z-10 top-0 py-4 bg-[#F8F8FF]">
            <div className="w-6xl class flex justify-between items-center">
              <h1 className="font-bold text-2xl">{baseInfo?.name}</h1>
              <div className="flex items-center gap-3">
                <button
                  className={`bg-gray-200 text-gray-500 font-semibold px-4 py-2 rounded-full hover:bg-gray-500 hover:text-white`}
                  onClick={handleDeletePracticeTest}
                >
                  Xoá bài kiểm tra
                </button>

                <button
                  className={`bg-indigo-500 text-white font-semibold px-4 py-2 rounded-full ${
                    changedQuestions.length > 0 ||
                    deleteOptions.length > 0 ||
                    deleteQuestions.length > 0 ||
                    (changedName &&
                      changedName?.name.length > 0 &&
                      changedName.name !== baseInfo?.name)
                      ? "cursor-pointer hover:bg-indigo-700"
                      : "pointer-events-none"
                  }`}
                  onClick={() => {
                    handleSaveChange(isFormValid);
                  }}
                >
                  Lưu
                </button>
              </div>
            </div>
          </div>

          {/* Thông tin chung */}
          <form onSubmit={(e) => e.preventDefault()}>
            <div className="mb-5">
              <h3>Tiêu đề</h3>
              <input
                type="text"
                name="name"
                placeholder={
                  changedName?.name.length === 0 && isSubmitted
                    ? "Vui lòng nhập tiêu đề"
                    : "Nhập tiêu đề"
                }
                className={`w-full bg-indigo-50 px-4 py-2 border ${
                  changedName?.name.length === 0 && isSubmitted
                    ? "border-red-500 bg-red-50 focus:outline-red-500"
                    : "border-gray-200"
                } focus:outline-1 focus:outline-indigo-500 rounded-md`}
                defaultValue={baseInfo?.name || ""}
                onBlur={(e) => handleBaseInfoChange(e)}
              />
            </div>
          </form>

          {/* Câu hỏi */}
          <form>
            <div className="flex flex-col gap-3">
              {questions.map((question, questionIndex) => {
                const changeQuestionType = changedQuestions.find(
                  (changedQuestion) => {
                    if (changedQuestion.id)
                      return changedQuestion.id === question.id;
                    return changedQuestion.tempId === question.tempId;
                  },
                )?.question?.type;
                const questionType =
                  changeQuestionType || question.question?.type;

                let isMissingQuestionBase: boolean = false;
                let showError = false;
                let isMissingOptionText = false;
                let hasCorrectAnswer = true;

                const changedQuestion = changedQuestions.find(
                  (changeQuestion) => {
                    if (changeQuestion.id) {
                      return changeQuestion.id === question.id;
                    }
                    return changeQuestion.tempId === question.tempId;
                  },
                );

                if (changedQuestion) {
                  const questionText = changedQuestion.question?.text || "";
                  isMissingQuestionBase = questionText.trim().length === 0;
                  showError = isMissingQuestionBase && isSubmitted;
                  isMissingOptionText = changedQuestion.options.some(
                    (option) => option.text.trim() === "",
                  );
                  hasCorrectAnswer = changedQuestion.options.some(
                    (option) => option.isCorrect === true,
                  );
                }

                return (
                  <div key={question.id ? question.id : question.tempId}>
                    {/* Quesiton Base */}
                    <div className="flex items-center gap-2 mb-2">
                      <p className="font-semibold text-gray-500">
                        {questionIndex + 1}.
                      </p>
                      <div className="w-full">
                        <input
                          type="text"
                          data-section="questionBase"
                          name="text"
                          defaultValue={question.question?.text}
                          className={`w-full px-3 py-1 border-b-2 ${
                            showError
                              ? "border-red-500 bg-red-50 focus:outline-1 focus:outline-red-500"
                              : "border-gray-200  focus:outline-0"
                          }`}
                          placeholder="Câu hỏi"
                          onBlur={(e) => {
                            if (question.question?.type) {
                              handleQuestionChange(
                                e,
                                questionIndex,
                                question.question.type,
                                null,
                              );
                            }
                          }}
                        />
                      </div>
                      <div
                        className={`p-1.5 bg-gray-50 rounded-full ${
                          questions.length > 2
                            ? "hover:bg-gray-300 cursor-pointer"
                            : "pointer-events-none"
                        }`}
                        onClick={() =>
                          handleDeleteCard(questionIndex, question.id)
                        }
                      >
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="18"
                          height="18"
                          viewBox="0 0 24 24"
                        >
                          <g fill="none" fillRule="evenodd">
                            <path d="m12.594 23.258l-.012.002l-.071.035l-.02.004l-.014-.004l-.071-.036q-.016-.004-.024.006l-.004.01l-.017.428l.005.02l.01.013l.104.074l.015.004l.012-.004l.104-.074l.012-.016l.004-.017l-.017-.427q-.004-.016-.016-.018m.264-.113l-.014.002l-.184.093l-.01.01l-.003.011l.018.43l.005.012l.008.008l.201.092q.019.005.029-.008l.004-.014l-.034-.614q-.005-.019-.02-.022m-.715.002a.02.02 0 0 0-.027.006l-.006.014l-.034.614q.001.018.017.024l.015-.002l.201-.093l.01-.008l.003-.011l.018-.43l-.003-.012l-.01-.01z" />
                            <path
                              fill={
                                questions.length > 2 ? "#374151" : "#9CA3AF"
                              }
                              d="M14.28 2a2 2 0 0 1 1.897 1.368L16.72 5H20a1 1 0 1 1 0 2h-1v12a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3V7H4a1 1 0 0 1 0-2h3.28l.543-1.632A2 2 0 0 1 9.721 2zM17 7H7v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1zm-2.72-3H9.72l-.333 1h5.226z"
                            />
                          </g>
                        </svg>
                      </div>
                    </div>

                    {/* Question Type */}
                    <div className="z-0 flex items-center justify-between">
                      <div className="relative">
                        <select
                          tabIndex={-1}
                          data-section="questionBase"
                          name="type"
                          defaultValue={question.question?.type}
                          className="appearance-none w-55 bg-indigo-50 border border-gray-200 text-gray-700 py-2 px-3 rounded-lg focus:outline-none  cursor-pointer"
                          onChange={(e) => {
                            if (question.question?.type) {
                              handleQuestionChange(
                                e,
                                questionIndex,
                                question.question.type,
                                null,
                              );
                            }
                          }}
                        >
                          <option value="SINGLE_CHOICE">Đáp án duy nhất</option>
                          <option value="MULTIPLE_CHOICE">Nhiều đáp án</option>
                          <option value="TRUE_FALSE">Đúng / Sai</option>
                        </select>
                        <div className="absolute top-3 right-3">
                          <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="18"
                            height="18"
                            viewBox="0 0 24 24"
                          >
                            <path
                              fill="none"
                              stroke="#374151"
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth="1.5"
                              d="m6 9l6 6l6-6"
                            />
                          </svg>
                        </div>
                      </div>

                      {isSubmitted &&
                      !hasCorrectAnswer &&
                      !isMissingQuestionBase &&
                      !isMissingOptionText ? (
                        <span className="font-semibold text-red-500">
                          Chọn đáp án đúng đê
                        </span>
                      ) : (
                        <>
                          {questionType !== "TRUE_FALSE" && (
                            <div
                              className={`p-1 rounded-full ${
                                question.options.length < 5
                                  ? "cursor-pointer hover:bg-gray-200"
                                  : "pointer-events-none"
                              }`}
                              onClick={() => handleAddOption(questionIndex)}
                            >
                              <svg
                                xmlns="http://www.w3.org/2000/svg"
                                width="18"
                                height="18"
                                viewBox="0 0 24 24"
                              >
                                <path
                                  fill={
                                    question.options.length < 5
                                      ? "#374151"
                                      : "#9CA3AF"
                                  }
                                  d="M11 13H6q-.425 0-.712-.288T5 12t.288-.712T6 11h5V6q0-.425.288-.712T12 5t.713.288T13 6v5h5q.425 0 .713.288T19 12t-.288.713T18 13h-5v5q0 .425-.288.713T12 19t-.712-.288T11 18z"
                                />
                              </svg>
                            </div>
                          )}
                        </>
                      )}
                    </div>

                    {questionType === "SINGLE_CHOICE" && (
                      <SingleChoice
                        question={changedQuestion ? changedQuestion : question}
                        isSubmitted={isSubmitted}
                        questionIndex={questionIndex}
                        handleQuestionChange={handleQuestionChange}
                        handleDeleteOption={handleDeleteOption}
                      />
                    )}
                    {questionType === "MULTIPLE_CHOICE" && (
                      <MultipleChoice
                        question={changedQuestion ? changedQuestion : question}
                        isSubmitted={isSubmitted}
                        questionIndex={questionIndex}
                        handleQuestionChange={handleQuestionChange}
                        handleDeleteOption={handleDeleteOption}
                      />
                    )}
                    {questionType === "TRUE_FALSE" && (
                      <TrueFalse
                        question={changedQuestion ? changedQuestion : question}
                        questionIndex={questionIndex}
                        handleQuestionChange={handleQuestionChange}
                      />
                    )}
                  </div>
                );
              })}

              <button
                type="button"
                className="my-5 w-fit mx-auto px-5 py-3 bg-gray-200 font-semibold rounded-full cursor-pointer hover:bg-gray-300"
                onClick={() => handleAddCard()}
              >
                Thêm thẻ
              </button>
            </div>
          </form>
        </section>
      </main>
    </>
  );
}
