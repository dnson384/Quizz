"use client";
import Header from "@/presentation/components/Layout/Header";
import SideMenu from "@/presentation/components/Layout/SideMenu";

import useMyCourse from "@/presentation/hooks/MyLib/useMyCourse";
export default function MyCourse() {
  const {
    // Data
    baseInfo,
    terms,
    changedName,
    changedTerms,
    // UI
    isLoading,
    isSubmitted,
    // Card Behavior
    handleDeleteCard,
    handleAddCard,
    // Input Change
    handleBaseInfoChange,
    handleTermChange,
    // Save
    handleSaveChange,
    handleDeleteCourse,
  } = useMyCourse();

  const titleMissing =
    changedName === undefined ||
    changedName.name.length === 0 ||
    changedName.name === baseInfo?.name;
  const anyMissing = changedTerms.some((changedTerm) => {
    if (changedTerm.term.length === 0) return true;
    if (changedTerm.definition.length === 0) return true;
  });
  const isFormValid = !titleMissing || (!anyMissing && changedTerms.length > 0);

  return (
    <>
      <Header />
      <main className="flex">
        <SideMenu />
        <div></div>
        {isLoading ? (
          <div className="w-full h-150 flex justify-center items-center">
            <span className="loader"></span>
          </div>
        ) : (
          <section className="mt-[74px] w-md sm:w-xl md:w-2xl lg:w-4xl mx-auto">
            <div className="sticky top-0 py-4 bg-[#F8F8FF]">
              <div className="w-full class flex justify-between items-center">
                <h1 className="font-bold text-2xl">{baseInfo?.name}</h1>
                <div className="flex items-center gap-3">
                  <button
                    className={`bg-gray-200 text-gray-500 font-semibold px-4 py-2 rounded-full cursor-pointer hover:bg-gray-500 hover:text-white`}
                    onClick={handleDeleteCourse}
                  >
                    Xoá học phần
                  </button>
                  <button
                    className={`bg-indigo-500 text-white font-semibold px-4 py-2 rounded-full ${
                      isFormValid
                        ? "cursor-pointer hover:bg-indigo-700"
                        : "pointer-events-none"
                    }`}
                    onClick={() => handleSaveChange(isFormValid)}
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
                  placeholder="Nhập tiêu đề"
                  className={`w-full bg-indigo-50 px-4 py-2 border ${
                    changedName?.name.length === 0 && isSubmitted
                      ? "border-red-500 bg-red-50 focus:outline-red-500"
                      : "border-gray-200"
                  } focus:outline-1 focus:outline-indigo-500 rounded-md`}
                  defaultValue={baseInfo?.name}
                  onBlur={(e) => handleBaseInfoChange(e)}
                />
                {changedName?.name.length === 0 && isSubmitted && (
                  <p className="text-red-500 text-xs">Vui lòng nhập tiêu đề</p>
                )}
              </div>
            </form>

            {/* Thuật ngữ */}
            <form>
              <div className="flex flex-col gap-3">
                {terms.map((term, index) => {
                  const missingTerm =
                    changedTerms.find(
                      (changedTerm) => changedTerm.id === term.id,
                    )?.term.length === 0 && isSubmitted;

                  const missingDef =
                    changedTerms.find(
                      (changedTerm) => changedTerm.id === term.id,
                    )?.definition.length === 0 && isSubmitted;

                  return (
                    <div
                      key={term.id !== null ? term.id : term.tempId}
                      className="px-6 py-4 bg-white rounded-2xl shadow-sm"
                    >
                      <div className="flex justify-between items-center mb-2">
                        <p className="font-semibold text-gray-500">
                          {index + 1}
                        </p>
                        <div
                          className={`p-1.5 bg-gray-50 rounded-full ${
                            terms.length > 2
                              ? "hover:bg-gray-300 cursor-pointer"
                              : "pointer-events-none"
                          }`}
                          onClick={() => handleDeleteCard(index)}
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
                                fill={terms.length > 2 ? "#374151" : "#9CA3AF"}
                                d="M14.28 2a2 2 0 0 1 1.897 1.368L16.72 5H20a1 1 0 1 1 0 2h-1v12a3 3 0 0 1-3 3H8a3 3 0 0 1-3-3V7H4a1 1 0 0 1 0-2h3.28l.543-1.632A2 2 0 0 1 9.721 2zM17 7H7v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1zm-2.72-3H9.72l-.333 1h5.226z"
                              />
                            </g>
                          </svg>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-5">
                        <div>
                          <input
                            type="text"
                            name="term"
                            className={`w-full bg-indigo-50 px-4 py-2 border ${
                              missingTerm
                                ? "border-red-500 bg-red-50 focus:outline-red-500"
                                : "border-gray-200"
                            } focus:outline-1 focus:outline-indigo-500 rounded-md`}
                            defaultValue={term.term}
                            onBlur={(e) => handleTermChange(e, index)}
                          />
                          <div className="flex items-center justify-between">
                            <p className="font-semibold text-gray-500">
                              Thuật ngữ
                            </p>
                            {missingTerm && (
                              <span className="text-red-500 text-xs">
                                Vui lòng nhập thuật ngữ này
                              </span>
                            )}
                          </div>
                        </div>
                        <div>
                          <input
                            type="text"
                            name="definition"
                            className={`w-full bg-indigo-50 px-4 py-2 border ${
                              missingDef
                                ? "border-red-500 bg-red-50 focus:outline-red-500"
                                : "border-gray-200"
                            } focus:outline-1 focus:outline-indigo-500 rounded-md`}
                            defaultValue={term.definition}
                            onBlur={(e) => handleTermChange(e, index)}
                          />
                          <div className="flex items-center justify-between">
                            <p className="font-semibold text-gray-500">
                              Định nghĩa
                            </p>
                            {missingDef && (
                              <span className="text-red-500 text-xs">
                                Vui lòng nhập định nghĩa này
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
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
        )}
      </main>
    </>
  );
}
